# -*- coding: utf-8 -*-
# Copyright (C) 2026 Patryk (Pates2004)
# SPDX-License-Identifier: GPL-2.0-or-later
"""Accessibility support for Autorun Organizer 6.x.

Autorun Organizer 6.x exposes its native VCL controls through UI Automation,
but controls rendered by Sciter are presented as one unnamed object per panel.
This module labels the native controls and turns those Sciter hosts into small,
keyboard-operable virtual controls. It also provides direct commands for the
most important areas of the application.
"""

import addonHandler
import appModuleHandler
import api
import controlTypes
import core
import mouseHandler
import ui
import winUser
from NVDAObjects.UIA import UIA
from logHandler import log
from scriptHandler import script


addonHandler.initTranslation()


_TOP_FILTERS = (
	(_("Important"), 0.22),
	(_("All"), 0.54),
	(_("Custom"), 0.83),
)

_DETAIL_TABS = (
	(_("Boot time"), 0.24),
	(_("Application"), 0.72),
)

_INTERNAL_NAMES = {
	"None",
	"Card1_1",
	"Card1_2",
	"Card2_1",
	"CardPanel1",
	"CardPanel2",
	"InfoPanelButtonsBarPanel",
	"Notifications",
	"ToggleSwitcher2Holder",
	"TopButtonsBarPanel",
}


def _uiaClassName(obj):
	"""Return the provider's UIA class, not the shared top-level HWND class."""
	try:
		return obj.UIAElement.CurrentClassName or ""
	except Exception:
		return ""


def _parentName(obj):
	try:
		return (obj.parent.name or "").strip()
	except Exception:
		return ""


def _locationTuple(obj):
	location = obj.location
	try:
		return location.left, location.top, location.width, location.height
	except AttributeError:
		return tuple(location)


class _ClickableSciterControl(UIA):
	"""Base overlay for a focusable Sciter host."""

	def _click(self, xRatio=0.5):
		return self.appModule._clickObject(self, xRatio=xRatio)


class _SciterToggle(_ClickableSciterControl):
	def _get_name(self):
		if _parentName(self) == "Notifications":
			return _("Notifications about new startup items")
		return _("Selected startup item state")

	def _get_role(self):
		return controlTypes.Role.CHECKBOX

	def script_activate(self, gesture):
		if self._click():
			ui.message(_("Toggled. The state will be applied by Autorun Organizer."))
		else:
			ui.message(_("Unable to activate the toggle."))

	__gestures = {
		"kb:enter": "activate",
		"kb:space": "activate",
	}


class _SciterSelector(_ClickableSciterControl):
	options = ()
	indexAttribute = ""
	title = ""

	def _get_role(self):
		return controlTypes.Role.TABCONTROL

	def _get_name(self):
		index = getattr(self.appModule, self.indexAttribute, 0)
		return f"{self.title}: {self.options[index][0]}"

	def _move(self, delta):
		index = getattr(self.appModule, self.indexAttribute, 0)
		index = (index + delta) % len(self.options)
		setattr(self.appModule, self.indexAttribute, index)
		ui.message(_("{label}, {position} of {count}").format(
			label=self.options[index][0],
			position=index + 1,
			count=len(self.options),
		))

	def script_previous(self, gesture):
		self._move(-1)

	def script_next(self, gesture):
		self._move(1)

	def script_activate(self, gesture):
		index = getattr(self.appModule, self.indexAttribute, 0)
		label, ratio = self.options[index]
		if self._click(ratio):
			ui.message(_("Selected: {label}").format(label=label))
		else:
			ui.message(_("Unable to select the item."))

	__gestures = {
		"kb:leftArrow": "previous",
		"kb:upArrow": "previous",
		"kb:rightArrow": "next",
		"kb:downArrow": "next",
		"kb:enter": "activate",
		"kb:space": "activate",
	}


class _TopFilterSelector(_SciterSelector):
	options = _TOP_FILTERS
	indexAttribute = "_topFilterIndex"
	title = _("View filter")


class _DetailTabSelector(_SciterSelector):
	options = _DETAIL_TABS
	indexAttribute = "_detailTabIndex"
	title = _("Details tab")


class AppModule(appModuleHandler.AppModule):
	scriptCategory = "Autorun Organizer"

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._topFilterIndex = 0
		self._detailTabIndex = 1
		self._readInitialView()

	def _readInitialView(self):
		try:
			import winreg

			with winreg.OpenKey(
				winreg.HKEY_CURRENT_USER,
				r"Software\ChemTable Software\Autorun Organizer\Settings",
			) as key:
				value = winreg.QueryValueEx(key, "ViewingModeEx3")[0]
			self._topFilterIndex = {
				"ImportantBtn": 0,
				"AllBtn": 1,
				"CustomBtn": 2,
			}.get(value, 0)
		except (OSError, ValueError):
			pass

	def isGoodUIAWindow(self, hwnd):
		# The VCL accessibility provider is useful here even though every object
		# shares the main window's HWND class.
		return True

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if not isinstance(obj, UIA) or _uiaClassName(obj) != "TSciterHostWindow":
			return
		parentName = _parentName(obj)
		if parentName in ("Notifications", "ToggleSwitcher2Holder"):
			clsList.insert(0, _SciterToggle)
		elif parentName == "TopButtonsBarPanel":
			clsList.insert(0, _TopFilterSelector)
		elif parentName == "InfoPanelButtonsBarPanel":
			clsList.insert(0, _DetailTabSelector)

	def event_NVDAObject_init(self, obj):
		try:
			className = _uiaClassName(obj)
			if className == "TButtonedEdit":
				obj.name = _("Search startup items")
			elif className == "TListView" and obj.role == controlTypes.Role.LIST:
				obj.name = _("Startup items")
			elif className == "TClickableLabelControl":
				obj.role = controlTypes.Role.BUTTON
		except Exception:
			log.debugWarning("Unable to improve an Autorun Organizer object", exc_info=True)

	def _walkForeground(self, maxObjects=300):
		try:
			root = api.getForegroundObject()
		except Exception:
			return
		stack = [root]
		seen = set()
		while stack and len(seen) < maxObjects:
			obj = stack.pop()
			identity = id(obj)
			if identity in seen:
				continue
			seen.add(identity)
			yield obj
			try:
				stack.extend(reversed(obj.children))
			except Exception:
				pass

	def _findObject(self, *, className=None, parentName=None, role=None, name=None):
		for obj in self._walkForeground():
			try:
				if className is not None and _uiaClassName(obj) != className:
					continue
				if parentName is not None and _parentName(obj) != parentName:
					continue
				if role is not None and obj.role != role:
					continue
				if name is not None and obj.name != name:
					continue
				return obj
			except Exception:
				continue
		return None

	def _clickObject(self, obj, xRatio=0.5, yRatio=0.5):
		try:
			left, top, width, height = _locationTuple(obj)
			if width <= 0 or height <= 0:
				raise ValueError("Empty control rectangle")
			x = int(left + width * xRatio)
			y = int(top + height * yRatio)
			oldX, oldY = winUser.getCursorPos()
			winUser.setCursorPos(x, y)
			mouseHandler.doPrimaryClick()
			core.callLater(80, winUser.setCursorPos, oldX, oldY)
			return True
		except Exception:
			log.error("Clicking an Autorun Organizer control failed", exc_info=True)
			return False

	def _clickSciter(self, parentName, ratio=0.5, successMessage=None):
		obj = self._findObject(className="TSciterHostWindow", parentName=parentName)
		if obj is None:
			ui.message(_("This control is not currently available in the application window."))
			return False
		if not self._clickObject(obj, xRatio=ratio):
			ui.message(_("Unable to activate the control."))
			return False
		if successMessage:
			ui.message(successMessage)
		return True

	def _focusObject(self, obj, missingMessage):
		if obj is None:
			ui.message(missingMessage)
			return
		try:
			obj.setFocus()
		except Exception:
			try:
				api.setNavigatorObject(obj)
				ui.message(obj.name or _("NVDA navigator object set"))
			except Exception:
				ui.message(_("Unable to move focus."))

	def _selectTopFilter(self, index):
		self._topFilterIndex = index
		label, ratio = _TOP_FILTERS[index]
		self._clickSciter("TopButtonsBarPanel", ratio, _("View: {label}").format(label=label))

	def _selectDetailTab(self, index):
		self._detailTabIndex = index
		label, ratio = _DETAIL_TABS[index]
		self._clickSciter("InfoPanelButtonsBarPanel", ratio, _("Tab: {label}").format(label=label))

	@script(description=_("Moves focus to the startup item list"), gesture="kb:NVDA+alt+l")
	def script_focusStartupList(self, gesture):
		obj = self._findObject(className="TListView", role=controlTypes.Role.LIST)
		self._focusObject(obj, _("The startup item list was not found."))

	@script(description=_("Moves focus to the search field"), gesture="kb:NVDA+alt+f")
	def script_focusSearch(self, gesture):
		obj = self._findObject(className="TButtonedEdit")
		self._focusObject(obj, _("The search field was not found."))

	@script(description=_("Selects the Important view"), gesture="kb:NVDA+alt+1")
	def script_viewImportant(self, gesture):
		self._selectTopFilter(0)

	@script(description=_("Selects the All view"), gesture="kb:NVDA+alt+2")
	def script_viewAll(self, gesture):
		self._selectTopFilter(1)

	@script(description=_("Selects the Custom view"), gesture="kb:NVDA+alt+3")
	def script_viewCustom(self, gesture):
		self._selectTopFilter(2)

	@script(description=_("Toggles application notifications"), gesture="kb:NVDA+alt+n")
	def script_toggleNotifications(self, gesture):
		self._clickSciter("Notifications", 0.5, _("Notification setting toggled."))

	@script(description=_("Enables or disables the selected startup item"), gesture="kb:NVDA+alt+s")
	def script_toggleStartupItem(self, gesture):
		self._clickSciter(
			"ToggleSwitcher2Holder",
			0.5,
			_("Selected startup item state toggled."),
		)

	@script(description=_("Opens the Boot time tab"), gesture="kb:NVDA+alt+b")
	def script_bootTimeTab(self, gesture):
		self._selectDetailTab(0)

	@script(description=_("Opens the Application tab"), gesture="kb:NVDA+alt+a")
	def script_applicationTab(self, gesture):
		self._selectDetailTab(1)

	@script(description=_("Reads available details for the selected item"), gesture="kb:NVDA+alt+d")
	def script_readDetails(self, gesture):
		parts = []
		focus = api.getFocusObject()
		if focus and focus.role == controlTypes.Role.LISTITEM and focus.name:
			parts.append(focus.name.strip())
		panel = self._findObject(name="CardPanel1")
		if panel is not None:
			stack = []
			try:
				stack.extend(reversed(panel.children))
			except Exception:
				pass
			while stack and len(parts) < 12:
				obj = stack.pop()
				try:
					name = (obj.name or "").strip()
					if name and name not in _INTERNAL_NAMES and name not in parts:
						parts.append(name)
					stack.extend(reversed(obj.children))
				except Exception:
					continue
		if parts:
			ui.message(". ".join(parts))
		else:
			ui.message(_("No details are available for the current item."))

	@script(description=_("Reports Autorun Organizer Access commands"), gesture="kb:NVDA+alt+h")
	def script_addonHelp(self, gesture):
		ui.message(
			_(
				"Add-on commands: NVDA plus Alt plus L, list; F, search; "
				"1, 2, 3, view filters; S, toggle selected item; "
				"N, notifications; A, application details; B, boot time; "
				"D, read details."
			)
		)
