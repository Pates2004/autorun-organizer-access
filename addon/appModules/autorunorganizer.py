# -*- coding: utf-8 -*-
# Copyright (C) 2026 Patryk (Pates2004)
# SPDX-License-Identifier: GPL-2.0-or-later
"""Accessibility support for the classic Autorun Organizer 6.x interface."""

import addonHandler
import appModuleHandler
import api
import controlTypes
import core
import keyboardHandler
import mouseHandler
import ui
import winUser
from NVDAObjects.UIA import UIA
from logHandler import log


_shared = addonHandler.getCodeAddon().loadModule("autorunOrganizerAccessShared")
tr = _shared.tr


_TOP_FILTERS = (
	("Important", 0.22),
	("All", 0.54),
	("Custom", 0.83),
)

_DETAIL_TABS = (
	("Boot time", 0.24),
	("Application", 0.72),
)

_TOP_ICON_NAMES = (
	"Notification center",
	"Settings and commands",
)

_STATUS_ACTION_NAMES = (
	"Interface theme",
	"Background functions",
	"Reviews",
	"Undo changes",
)

_INTERNAL_NAMES = {
	"None",
	"Card1_1",
	"Card1_2",
	"Card1_3",
	"Card1_5",
	"Card1_6",
	"Card2_1",
	"CardPanel1",
	"CardPanel2",
	"InfoPanelButtonsBarPanel",
	"Measure each system load time",
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


def _hasAncestorClass(obj, className, maxDepth=12):
	current = obj
	for _depth in range(maxDepth):
		if current is None:
			return False
		if _uiaClassName(current) == className:
			return True
		try:
			current = current.parent
		except Exception:
			return False
	return False


def _locationTuple(obj):
	location = obj.location
	try:
		return location.left, location.top, location.width, location.height
	except AttributeError:
		return tuple(location)


def _horizontalRatioInParent(obj):
	try:
		left, _top, width, _height = _locationTuple(obj)
		parentLeft, _parentTop, parentWidth, _parentHeight = _locationTuple(obj.parent)
		if parentWidth <= 0:
			return None
		return ((left + width / 2) - parentLeft) / parentWidth
	except Exception:
		return None


def _topIconIndex(obj):
	"""Classify the two unlabeled icon panels to the right of the search box."""
	if _uiaClassName(obj) != "TPanel" or _uiaClassName(getattr(obj, "parent", None)) != "TStackPanel":
		return None
	try:
		_left, _top, width, height = _locationTuple(obj)
		_parentLeft, _parentTop, parentWidth, parentHeight = _locationTuple(obj.parent)
	except Exception:
		return None
	if (
		width <= 0
		or height <= 0
		or parentWidth <= 0
		or parentHeight <= 0
		or width / parentWidth > 0.32
		or height / parentHeight > 1.5
	):
		return None
	ratio = _horizontalRatioInParent(obj)
	if ratio is None or ratio < 0.65:
		return None
	return 0 if ratio < 0.86 else 1


def _statusActionIndex(obj):
	"""Classify the four unlabeled action panels in the status bar."""
	if _uiaClassName(obj) != "TPanel" or _uiaClassName(getattr(obj, "parent", None)) != "TStatusBar":
		return None
	try:
		_left, _top, width, height = _locationTuple(obj)
		_parentLeft, _parentTop, parentWidth, parentHeight = _locationTuple(obj.parent)
	except Exception:
		return None
	if height <= 0 or parentHeight <= 0 or parentWidth <= 0 or height / parentHeight > 1.5:
		return None
	ratio = _horizontalRatioInParent(obj)
	if ratio is None:
		return None
	widthRatio = width / parentWidth
	if widthRatio <= 0.09:
		if 0.54 <= ratio < 0.61:
			return 0
		if 0.61 <= ratio < 0.68:
			return 1
	elif widthRatio >= 0.1:
		if 0.68 <= ratio < 0.84:
			return 2
		if ratio >= 0.84:
			return 3
	return None


def _isObjectVisible(obj):
	try:
		if obj.UIAElement.CurrentIsOffscreen:
			return False
	except Exception:
		pass
	try:
		hwnd = int(obj.UIAElement.CurrentNativeWindowHandle or 0)
		if hwnd and not winUser.isWindowVisible(hwnd):
			return False
	except Exception:
		pass
	try:
		_left, _top, width, height = _locationTuple(obj)
		return width > 0 and height > 0
	except Exception:
		return True


class _ClickableControl(UIA):
	"""Base overlay for controls which need a mouse-backed default action."""

	def _click(self, xRatio=0.5):
		return self.appModule._clickObject(self, xRatio=xRatio)

	def script_activate(self, gesture):
		if not self._click():
			ui.message(tr("Unable to activate the control."))

	__gestures = {
		"kb:enter": "activate",
		"kb:space": "activate",
	}


class _NativeClickableLabel(_ClickableControl):
	def _get_role(self):
		return controlTypes.Role.BUTTON


class _GroupButton(_ClickableControl):
	def _get_role(self):
		return controlTypes.Role.RADIOBUTTON


class _TopIconButton(_ClickableControl):
	def _get_name(self):
		index = _topIconIndex(self)
		return tr(_TOP_ICON_NAMES[index]) if index is not None else tr("Autorun Organizer action")

	def _get_role(self):
		return controlTypes.Role.BUTTON


class _StatusActionButton(_ClickableControl):
	def _get_name(self):
		index = _statusActionIndex(self)
		return tr(_STATUS_ACTION_NAMES[index]) if index is not None else tr("Autorun Organizer status action")

	def _get_role(self):
		return controlTypes.Role.BUTTON


class _SciterActionButton(_ClickableControl):
	def _get_name(self):
		parentName = _parentName(self)
		if _shared.matchesApplicationText(parentName, "Notifications"):
			return tr("Enable or disable notifications about new startup items")
		if _shared.matchesApplicationText(parentName, "Measure each system load time"):
			return tr("Enable or disable measuring every system startup")
		if parentName == "ToggleSwitcher2Holder":
			return tr("Enable or disable the selected startup item")
		return tr("Autorun Organizer switch")

	def _get_role(self):
		# Sciter exposes no checked state. Reporting this as a check box makes
		# NVDA incorrectly announce "unchecked", so expose an action button.
		return controlTypes.Role.BUTTON

	def script_activate(self, gesture):
		if self._click():
			ui.message(tr("Command sent. Autorun Organizer does not expose the resulting state to NVDA."))
		else:
			ui.message(tr("Unable to activate the control."))


class _SciterSelector(_ClickableControl):
	options = ()
	indexAttribute = ""
	title = ""

	def _get_role(self):
		return controlTypes.Role.TABCONTROL

	def _get_name(self):
		index = getattr(self.appModule, self.indexAttribute, 0)
		return f"{tr(self.title)}: {tr(self.options[index][0])}"

	def _move(self, delta):
		index = getattr(self.appModule, self.indexAttribute, 0)
		index = (index + delta) % len(self.options)
		setattr(self.appModule, self.indexAttribute, index)
		ui.message(
			tr(
				"{label}, {position} of {count}",
				label=tr(self.options[index][0]),
				position=index + 1,
				count=len(self.options),
			),
		)

	def script_previous(self, gesture):
		self._move(-1)

	def script_next(self, gesture):
		self._move(1)

	def script_activate(self, gesture):
		index = getattr(self.appModule, self.indexAttribute, 0)
		label, ratio = self.options[index]
		if self._click(ratio):
			ui.message(tr("Selected: {label}", label=tr(label)))
		else:
			ui.message(tr("Unable to select the item."))

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
	title = "View filter"


class _DetailTabSelector(_SciterSelector):
	options = _DETAIL_TABS
	indexAttribute = "_detailTabIndex"
	title = "Details tab"


class AppModule(appModuleHandler.AppModule):
	"""NVDA app module for every classic Autorun Organizer 6.x window."""

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._topFilterIndex = 0
		self._detailTabIndex = 1
		self._readInitialView()

	@property
	def isSupportedVersion(self):
		version = str(getattr(self, "productVersion", "") or "").strip()
		return not version or version.startswith("6.")

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
		# Autorun Organizer's standard popup menus expose names and checked
		# states correctly through MSAA.  Forcing UIA on the system menu window
		# (#32768) loses those states on some NVDA/Windows combinations.
		return winUser.getClassName(hwnd) != "#32768"

	def isBadUIAWindow(self, hwnd):
		# Explicitly keep popup menus on the same MSAA path NVDA uses when the
		# add-on is disabled. isGoodUIAWindow takes precedence, so both methods
		# must agree for this window class.
		return winUser.getClassName(hwnd) == "#32768"

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if not self.isSupportedVersion or not isinstance(obj, UIA):
			return
		className = _uiaClassName(obj)
		if className == "TSciterHostWindow":
			parentName = _parentName(obj)
			if parentName == "ToggleSwitcher2Holder" or any(
				_shared.matchesApplicationText(parentName, sourceName)
				for sourceName in ("Notifications", "Measure each system load time")
			):
				clsList.insert(0, _SciterActionButton)
			elif parentName == "TopButtonsBarPanel":
				clsList.insert(0, _TopFilterSelector)
			elif parentName == "InfoPanelButtonsBarPanel":
				clsList.insert(0, _DetailTabSelector)
		elif className == "TClickableLabelControl":
			clsList.insert(0, _NativeClickableLabel)
		elif className == "TGroupButton":
			clsList.insert(0, _GroupButton)
		elif _topIconIndex(obj) is not None:
			clsList.insert(0, _TopIconButton)
		elif _statusActionIndex(obj) is not None:
			clsList.insert(0, _StatusActionButton)

	def event_NVDAObject_init(self, obj):
		if not self.isSupportedVersion:
			return
		try:
			className = _uiaClassName(obj)
			if className == "TButtonedEdit" and _hasAncestorClass(obj, "TStartupManagerFrame"):
				obj.name = tr("Search startup items")
			elif (
				className == "TListView"
				and obj.role == controlTypes.Role.LIST
				and _hasAncestorClass(obj, "TStartupManagerFrame")
			):
				obj.name = tr("Startup items")
			elif (
				className == "TStatusBar"
				and _hasAncestorClass(obj, "TAutorunOrganizerMainForm")
				and not (obj.name or "").strip()
			):
				obj.name = tr("Autorun Organizer status")
			elif className == "TTreeView" and not (obj.name or "").strip():
				if _hasAncestorClass(obj, "TSettingsForm"):
					obj.name = tr("Settings categories")
				elif _hasAncestorClass(obj, "TUndoingChangesCenterForm"):
					obj.name = tr("Objects affected by the selected change")
			elif (
				className == "TControlList"
				and _hasAncestorClass(obj, "TUndoingChangesCenterForm")
				and not (obj.name or "").strip()
			):
				obj.name = tr("Changes that can be undone")
			elif (
				className == "TPageControl"
				and _hasAncestorClass(obj, "TNewStartupItemForm")
				and not (obj.name or "").strip()
			):
				obj.name = tr("Startup entry type")
			name = (obj.name or "").strip()
			if (
				name
				and name not in _INTERNAL_NAMES
				and getattr(obj, "role", None) != controlTypes.Role.LISTITEM
			):
				obj.name = _shared.translateApplicationText(obj.name)
		except Exception:
			log.debugWarning("Unable to improve an Autorun Organizer object", exc_info=True)

	def _walkForeground(self, maxObjects=600):
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

	def _findObject(self, *, className=None, parentName=None, role=None, name=None, visibleOnly=False):
		for obj in self._walkForeground():
			try:
				if className is not None and _uiaClassName(obj) != className:
					continue
				if parentName is not None and not _shared.matchesApplicationText(_parentName(obj), parentName):
					continue
				if role is not None and obj.role != role:
					continue
				if name is not None and obj.name != name:
					continue
				if visibleOnly and not _isObjectVisible(obj):
					continue
				return obj
			except Exception:
				continue
		return None

	def _findClassifiedPanel(self, classifier, index):
		for obj in self._walkForeground():
			try:
				if classifier(obj) == index and _isObjectVisible(obj):
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
		obj = self._findObject(
			className="TSciterHostWindow",
			parentName=parentName,
			visibleOnly=True,
		)
		if obj is None:
			ui.message(tr("This control is not currently available in the application window."))
			return False
		if not self._clickObject(obj, xRatio=ratio):
			ui.message(tr("Unable to activate the control."))
			return False
		if successMessage:
			ui.message(successMessage)
		return True

	def _focusObject(self, obj, missingMessage):
		if obj is None:
			ui.message(missingMessage)
			return False
		try:
			obj.setFocus()
			return True
		except Exception:
			try:
				api.setNavigatorObject(obj)
				ui.message(obj.name or tr("NVDA navigator object set"))
				return True
			except Exception:
				ui.message(tr("Unable to move focus."))
				return False

	def _clickTopIcon(self, index):
		obj = self._findClassifiedPanel(_topIconIndex, index)
		if obj is None or not self._clickObject(obj):
			ui.message(tr("{name} is not currently available.", name=tr(_TOP_ICON_NAMES[index])))
			return False
		ui.message(tr("Opened {name}.", name=tr(_TOP_ICON_NAMES[index])))
		return True

	def _clickStatusAction(self, index):
		obj = self._findClassifiedPanel(_statusActionIndex, index)
		if obj is None or not self._clickObject(obj):
			ui.message(tr("{name} is not currently available.", name=tr(_STATUS_ACTION_NAMES[index])))
			return False
		ui.message(tr("Activated {name}.", name=tr(_STATUS_ACTION_NAMES[index])))
		return True

	def _selectTopFilter(self, index):
		self._topFilterIndex = index
		label, ratio = _TOP_FILTERS[index]
		return self._clickSciter("TopButtonsBarPanel", ratio, tr("View: {label}", label=tr(label)))

	def _selectDetailTab(self, index):
		self._detailTabIndex = index
		label, ratio = _DETAIL_TABS[index]
		return self._clickSciter("InfoPanelButtonsBarPanel", ratio, tr("Tab: {label}", label=tr(label)))

	def _sendKey(self, keyName):
		try:
			keyboardHandler.KeyboardInputGesture.fromName(keyName).send()
		except Exception:
			log.error("Sending an Autorun Organizer keyboard command failed", exc_info=True)
			ui.message(tr("Unable to send the keyboard command."))

	def focusStartupList(self):
		obj = self._findObject(className="TListView", role=controlTypes.Role.LIST, visibleOnly=True)
		self._focusObject(obj, tr("The startup item list was not found."))

	def focusSearch(self):
		obj = self._findObject(className="TButtonedEdit", visibleOnly=True)
		self._focusObject(obj, tr("The search field was not found."))

	def viewImportant(self):
		self._selectTopFilter(0)

	def viewAll(self):
		self._selectTopFilter(1)

	def viewCustom(self):
		self._selectTopFilter(2)

	def openStartupLocations(self):
		self._topFilterIndex = 2
		if self._clickSciter("TopButtonsBarPanel", 0.97):
			ui.message(tr("Startup locations menu opened."))

	def toggleNotifications(self):
		self._clickSciter(
			"Notifications",
			0.5,
			tr("Notification command sent. The resulting state is not exposed to NVDA."),
		)

	def openNotificationCenter(self):
		self._clickTopIcon(0)

	def toggleStartupItem(self):
		if self._selectDetailTab(1):
			core.callLater(
				140,
				self._clickSciter,
				"ToggleSwitcher2Holder",
				0.5,
				tr("Startup item command sent. The resulting enabled or disabled state is not exposed to NVDA."),
			)

	def openSelectedItemMenu(self):
		focus = api.getFocusObject()
		if getattr(focus, "role", None) == controlTypes.Role.LISTITEM:
			self._sendKey("shift+f10")
			return
		obj = self._findObject(className="TListView", role=controlTypes.Role.LIST, visibleOnly=True)
		if self._focusObject(obj, tr("The startup item list was not found.")):
			core.callLater(100, self._sendKey, "shift+f10")

	def bootTimeTab(self):
		self._selectDetailTab(0)

	def applicationTab(self):
		self._selectDetailTab(1)

	def toggleMeasureEachBoot(self):
		if self._selectDetailTab(0):
			core.callLater(
				140,
				self._clickSciter,
				"Measure each system load time",
				0.5,
				tr("Measurement command sent. The resulting state is not exposed to NVDA."),
			)

	def readDetails(self):
		parts = []
		focus = api.getFocusObject()
		if focus and focus.role == controlTypes.Role.LISTITEM and focus.name:
			parts.append(focus.name.strip())
		panel = self._findObject(className="TCardPanel", name="CardPanel1", visibleOnly=True)
		if panel is not None:
			stack = []
			try:
				stack.extend(reversed(panel.children))
			except Exception:
				pass
			seen = set(parts)
			while stack and len(parts) < 30:
				obj = stack.pop()
				try:
					if not _isObjectVisible(obj):
						continue
					name = (obj.name or "").strip()
					if name and name not in _INTERNAL_NAMES and name not in seen:
						parts.append(name)
						seen.add(name)
					stack.extend(reversed(obj.children))
				except Exception:
					continue
		if parts:
			ui.message(". ".join(parts))
		else:
			ui.message(tr("No details are available for the current item or tab."))

	def openMainMenu(self):
		self._clickTopIcon(1)

	def openUndoChanges(self):
		self._clickStatusAction(3)

	def openReviews(self):
		self._clickStatusAction(2)

	def toggleTheme(self):
		self._clickStatusAction(0)

	def openBackgroundFunctions(self):
		self._clickStatusAction(1)

	def focusRebootAndMeasure(self):
		if self._selectDetailTab(0):
			core.callLater(140, self._focusNamedButton, "Reboot and measure")

	def _focusNamedButton(self, namePrefix):
		for obj in self._walkForeground():
			try:
				if (
					_uiaClassName(obj) == "TButton"
					and _shared.startsWithApplicationText(obj.name, namePrefix)
					and _isObjectVisible(obj)
				):
					self._focusObject(obj, "")
					return
			except Exception:
				continue
		ui.message(tr("The {name} button was not found.", name=tr(namePrefix)))

	def focusFrequencyDisplay(self):
		obj = None
		for candidate in self._walkForeground():
			try:
				if (
					_uiaClassName(candidate) == "TButton"
					and _shared.matchesApplicationText(candidate.name, "Display")
					and _isObjectVisible(candidate)
				):
					obj = candidate
					break
			except Exception:
				continue
		self._focusObject(obj, tr("The disable and delay frequency button was not found."))
