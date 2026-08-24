# -*- coding: utf-8 -*-
# Copyright (C) 2026 Patryk (Pates2004)
# SPDX-License-Identifier: GPL-2.0-or-later
"""Globally discoverable, application-scoped commands for Autorun Organizer 6.x."""

import addonHandler
import api
import config
import globalPluginHandler
import gui
import ui
import wx
from scriptHandler import script


_shared = addonHandler.getCodeAddon().loadModule("autorunOrganizerAccessShared")
_shared.registerConfig()
tr = _shared.tr
SCRIPT_CATEGORY = "Autorun Organizer Access"


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	"""Expose commands in Input Gestures while activating them only in 6.x."""

	scriptCategory = SCRIPT_CATEGORY

	def __init__(self):
		super().__init__()
		categories = gui.settingsDialogs.NVDASettingsDialog.categoryClasses
		if AutorunOrganizerAccessSettingsPanel not in categories:
			categories.append(AutorunOrganizerAccessSettingsPanel)
		_refreshScriptDescriptions()

	def terminate(self):
		categories = gui.settingsDialogs.NVDASettingsDialog.categoryClasses
		if AutorunOrganizerAccessSettingsPanel in categories:
			categories.remove(AutorunOrganizerAccessSettingsPanel)
		super().terminate()

	def _getAppModule(self):
		try:
			focus = api.getFocusObject()
			appModule = focus.appModule
		except Exception:
			return None
		if getattr(appModule, "appName", "") != "autorunorganizer":
			return None
		if not getattr(appModule, "isSupportedVersion", False):
			return None
		return appModule

	def getScript(self, gesture):
		scriptToRun = super().getScript(gesture)
		if scriptToRun is not None and self._getAppModule() is None:
			# The commands remain globally visible in Input Gestures, but their
			# default or user-assigned keys do not shadow other applications.
			return None
		return scriptToRun

	def _callApp(self, methodName):
		appModule = self._getAppModule()
		if appModule is None:
			ui.message(tr("Autorun Organizer 6.x is not active."))
			return
		method = getattr(appModule, methodName, None)
		if method is None:
			ui.message(tr("This command is not available in the current Autorun Organizer window."))
			return
		method()

	@script(
		description=tr("Move focus to the startup item list"),
		category=SCRIPT_CATEGORY,
		gesture="kb:NVDA+alt+l",
	)
	def script_focusStartupList(self, gesture):
		self._callApp("focusStartupList")

	@script(description=tr("Move focus to the search field"), category=SCRIPT_CATEGORY, gesture="kb:NVDA+alt+f")
	def script_focusSearch(self, gesture):
		self._callApp("focusSearch")

	@script(description=tr("Select the Important view"), category=SCRIPT_CATEGORY, gesture="kb:NVDA+alt+1")
	def script_viewImportant(self, gesture):
		self._callApp("viewImportant")

	@script(description=tr("Select the All view"), category=SCRIPT_CATEGORY, gesture="kb:NVDA+alt+2")
	def script_viewAll(self, gesture):
		self._callApp("viewAll")

	@script(description=tr("Select the Custom view"), category=SCRIPT_CATEGORY, gesture="kb:NVDA+alt+3")
	def script_viewCustom(self, gesture):
		self._callApp("viewCustom")

	@script(
		description=tr("Open the startup locations menu"),
		category=SCRIPT_CATEGORY,
		gesture="kb:NVDA+alt+4",
	)
	def script_openStartupLocations(self, gesture):
		self._callApp("openStartupLocations")

	@script(
		description=tr("Enable or disable the selected startup item"),
		category=SCRIPT_CATEGORY,
		gesture="kb:NVDA+alt+s",
	)
	def script_toggleStartupItem(self, gesture):
		self._callApp("toggleStartupItem")

	@script(
		description=tr("Open commands for the selected startup item"),
		category=SCRIPT_CATEGORY,
		gesture="kb:NVDA+alt+c",
	)
	def script_openSelectedItemMenu(self, gesture):
		self._callApp("openSelectedItemMenu")

	@script(
		description=tr("Toggle notifications about new startup items"),
		category=SCRIPT_CATEGORY,
		gesture="kb:NVDA+alt+n",
	)
	def script_toggleNotifications(self, gesture):
		self._callApp("toggleNotifications")

	@script(
		description=tr("Open the notification center"),
		category=SCRIPT_CATEGORY,
		gesture="kb:NVDA+alt+shift+n",
	)
	def script_openNotificationCenter(self, gesture):
		self._callApp("openNotificationCenter")

	@script(description=tr("Open the Boot time tab"), category=SCRIPT_CATEGORY, gesture="kb:NVDA+alt+b")
	def script_bootTimeTab(self, gesture):
		self._callApp("bootTimeTab")

	@script(description=tr("Open the Application tab"), category=SCRIPT_CATEGORY, gesture="kb:NVDA+alt+a")
	def script_applicationTab(self, gesture):
		self._callApp("applicationTab")

	@script(
		description=tr("Toggle measuring every system load time"),
		category=SCRIPT_CATEGORY,
		gesture="kb:NVDA+alt+shift+b",
	)
	def script_toggleMeasureEachBoot(self, gesture):
		self._callApp("toggleMeasureEachBoot")

	@script(
		description=tr("Read details for the selected item or current details tab"),
		category=SCRIPT_CATEGORY,
		gesture="kb:NVDA+alt+d",
	)
	def script_readDetails(self, gesture):
		self._callApp("readDetails")

	@script(
		description=tr("Open Settings and commands"),
		category=SCRIPT_CATEGORY,
		gesture="kb:NVDA+alt+m",
	)
	def script_openMainMenu(self, gesture):
		self._callApp("openMainMenu")

	@script(description=tr("Open Undo changes"), category=SCRIPT_CATEGORY, gesture="kb:NVDA+alt+u")
	def script_openUndoChanges(self, gesture):
		self._callApp("openUndoChanges")

	@script(description=tr("Open reviews"), category=SCRIPT_CATEGORY)
	def script_openReviews(self, gesture):
		self._callApp("openReviews")

	@script(description=tr("Toggle the Autorun Organizer interface theme"), category=SCRIPT_CATEGORY)
	def script_toggleTheme(self, gesture):
		self._callApp("toggleTheme")

	@script(description=tr("Open Background functions"), category=SCRIPT_CATEGORY)
	def script_openBackgroundFunctions(self, gesture):
		self._callApp("openBackgroundFunctions")

	@script(description=tr("Move focus to Reboot and measure"), category=SCRIPT_CATEGORY)
	def script_focusRebootAndMeasure(self, gesture):
		self._callApp("focusRebootAndMeasure")

	@script(description=tr("Move focus to disable and delay frequency"), category=SCRIPT_CATEGORY)
	def script_focusFrequencyDisplay(self, gesture):
		self._callApp("focusFrequencyDisplay")

	@script(
		description=tr("Report Autorun Organizer Access commands"),
		category=SCRIPT_CATEGORY,
		gesture="kb:NVDA+alt+h",
	)
	def script_addonHelp(self, gesture):
		ui.message(
			tr(
				"Commands: NVDA plus Alt plus L, list; F, search; 1, 2, 3, filters; "
				"4, startup locations; S, toggle item; C, item commands; N, notification toggle; "
				"Shift N, notification center; A, Application tab; B, Boot time; Shift B, measure each boot; "
				"D, details; M, settings and commands; U, undo changes; H, help. "
				"Every command can be reassigned in NVDA Input Gestures."
			)
		)


class AutorunOrganizerAccessSettingsPanel(gui.settingsDialogs.SettingsPanel):
	"""Language settings independent from NVDA's own interface language."""

	title = SCRIPT_CATEGORY

	def makeSettings(self, panelSizer):
		helper = gui.guiHelper.BoxSizerHelper(self, sizer=panelSizer)
		language = _shared.resolveLanguage()
		self._modes = _shared.LANGUAGE_MODES
		self.languageChoice = helper.addLabeledControl(
			tr(
				"Language used for add-on messages and Autorun Organizer text spoken by NVDA:",
				language=language,
			),
			wx.Choice,
			choices=list(_shared.languageModeLabels(language)),
		)
		try:
			selection = self._modes.index(_shared.getConfiguredMode())
		except ValueError:
			selection = 0
		self.languageChoice.SetSelection(selection)
		helper.addItem(
			wx.StaticText(
				self,
				label=tr(
					"Windows and application languages other than Polish use English. The setting changes what "
					"NVDA speaks and displays on a braille display; it does not change text drawn visually by "
					"Autorun Organizer.",
					language=language,
				),
			)
		)

	def onSave(self):
		selection = self.languageChoice.GetSelection()
		if selection < 0 or selection >= len(self._modes):
			selection = 0
		config.conf[_shared.CONFIG_SECTION]["language"] = self._modes[selection]
		_refreshScriptDescriptions()


_SCRIPT_DESCRIPTION_KEYS = {
	"focusStartupList": "Move focus to the startup item list",
	"focusSearch": "Move focus to the search field",
	"viewImportant": "Select the Important view",
	"viewAll": "Select the All view",
	"viewCustom": "Select the Custom view",
	"openStartupLocations": "Open the startup locations menu",
	"toggleStartupItem": "Enable or disable the selected startup item",
	"openSelectedItemMenu": "Open commands for the selected startup item",
	"toggleNotifications": "Toggle notifications about new startup items",
	"openNotificationCenter": "Open the notification center",
	"bootTimeTab": "Open the Boot time tab",
	"applicationTab": "Open the Application tab",
	"toggleMeasureEachBoot": "Toggle measuring every system load time",
	"readDetails": "Read details for the selected item or current details tab",
	"openMainMenu": "Open Settings and commands",
	"openUndoChanges": "Open Undo changes",
	"openReviews": "Open reviews",
	"toggleTheme": "Toggle the Autorun Organizer interface theme",
	"openBackgroundFunctions": "Open Background functions",
	"focusRebootAndMeasure": "Move focus to Reboot and measure",
	"focusFrequencyDisplay": "Move focus to disable and delay frequency",
	"addonHelp": "Report Autorun Organizer Access commands",
}


def _refreshScriptDescriptions():
	for scriptName, description in _SCRIPT_DESCRIPTION_KEYS.items():
		getattr(GlobalPlugin, f"script_{scriptName}").__doc__ = tr(description)


_refreshScriptDescriptions()
