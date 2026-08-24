# -*- coding: utf-8 -*-
# Copyright (C) 2026 Patryk (Pates2004)
# SPDX-License-Identifier: GPL-2.0-or-later
"""Globally discoverable, application-scoped commands for Autorun Organizer 6.x."""

import api
import globalPluginHandler
import ui
from scriptHandler import script


SCRIPT_CATEGORY = "Autorun Organizer Access"


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	"""Expose commands in Input Gestures while activating them only in 6.x."""

	scriptCategory = SCRIPT_CATEGORY

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
			ui.message("Autorun Organizer 6.x is not active.")
			return
		method = getattr(appModule, methodName, None)
		if method is None:
			ui.message("This command is not available in the current Autorun Organizer window.")
			return
		method()

	@script(
		description="Move focus to the startup item list", category=SCRIPT_CATEGORY, gesture="kb:NVDA+alt+l"
	)
	def script_focusStartupList(self, gesture):
		self._callApp("focusStartupList")

	@script(description="Move focus to the search field", category=SCRIPT_CATEGORY, gesture="kb:NVDA+alt+f")
	def script_focusSearch(self, gesture):
		self._callApp("focusSearch")

	@script(description="Select the Important view", category=SCRIPT_CATEGORY, gesture="kb:NVDA+alt+1")
	def script_viewImportant(self, gesture):
		self._callApp("viewImportant")

	@script(description="Select the All view", category=SCRIPT_CATEGORY, gesture="kb:NVDA+alt+2")
	def script_viewAll(self, gesture):
		self._callApp("viewAll")

	@script(description="Select the Custom view", category=SCRIPT_CATEGORY, gesture="kb:NVDA+alt+3")
	def script_viewCustom(self, gesture):
		self._callApp("viewCustom")

	@script(
		description="Open the startup locations menu",
		category=SCRIPT_CATEGORY,
		gesture="kb:NVDA+alt+4",
	)
	def script_openStartupLocations(self, gesture):
		self._callApp("openStartupLocations")

	@script(
		description="Enable or disable the selected startup item",
		category=SCRIPT_CATEGORY,
		gesture="kb:NVDA+alt+s",
	)
	def script_toggleStartupItem(self, gesture):
		self._callApp("toggleStartupItem")

	@script(
		description="Open commands for the selected startup item",
		category=SCRIPT_CATEGORY,
		gesture="kb:NVDA+alt+c",
	)
	def script_openSelectedItemMenu(self, gesture):
		self._callApp("openSelectedItemMenu")

	@script(
		description="Toggle notifications about new startup items",
		category=SCRIPT_CATEGORY,
		gesture="kb:NVDA+alt+n",
	)
	def script_toggleNotifications(self, gesture):
		self._callApp("toggleNotifications")

	@script(
		description="Open the notification center",
		category=SCRIPT_CATEGORY,
		gesture="kb:NVDA+alt+shift+n",
	)
	def script_openNotificationCenter(self, gesture):
		self._callApp("openNotificationCenter")

	@script(description="Open the Boot time tab", category=SCRIPT_CATEGORY, gesture="kb:NVDA+alt+b")
	def script_bootTimeTab(self, gesture):
		self._callApp("bootTimeTab")

	@script(description="Open the Application tab", category=SCRIPT_CATEGORY, gesture="kb:NVDA+alt+a")
	def script_applicationTab(self, gesture):
		self._callApp("applicationTab")

	@script(
		description="Toggle measuring every system load time",
		category=SCRIPT_CATEGORY,
		gesture="kb:NVDA+alt+shift+b",
	)
	def script_toggleMeasureEachBoot(self, gesture):
		self._callApp("toggleMeasureEachBoot")

	@script(
		description="Read details for the selected item or current details tab",
		category=SCRIPT_CATEGORY,
		gesture="kb:NVDA+alt+d",
	)
	def script_readDetails(self, gesture):
		self._callApp("readDetails")

	@script(
		description="Open Settings and commands",
		category=SCRIPT_CATEGORY,
		gesture="kb:NVDA+alt+m",
	)
	def script_openMainMenu(self, gesture):
		self._callApp("openMainMenu")

	@script(description="Open Undo changes", category=SCRIPT_CATEGORY, gesture="kb:NVDA+alt+u")
	def script_openUndoChanges(self, gesture):
		self._callApp("openUndoChanges")

	@script(description="Open reviews", category=SCRIPT_CATEGORY)
	def script_openReviews(self, gesture):
		self._callApp("openReviews")

	@script(description="Toggle the Autorun Organizer interface theme", category=SCRIPT_CATEGORY)
	def script_toggleTheme(self, gesture):
		self._callApp("toggleTheme")

	@script(description="Open Background functions", category=SCRIPT_CATEGORY)
	def script_openBackgroundFunctions(self, gesture):
		self._callApp("openBackgroundFunctions")

	@script(description="Move focus to Reboot and measure", category=SCRIPT_CATEGORY)
	def script_focusRebootAndMeasure(self, gesture):
		self._callApp("focusRebootAndMeasure")

	@script(description="Move focus to disable and delay frequency", category=SCRIPT_CATEGORY)
	def script_focusFrequencyDisplay(self, gesture):
		self._callApp("focusFrequencyDisplay")

	@script(
		description="Report Autorun Organizer Access commands",
		category=SCRIPT_CATEGORY,
		gesture="kb:NVDA+alt+h",
	)
	def script_addonHelp(self, gesture):
		ui.message(
			"Commands: NVDA plus Alt plus L, list; F, search; 1, 2, 3, filters; "
			"4, startup locations; S, toggle item; C, item commands; N, notification toggle; "
			"Shift N, notification center; A, Application tab; B, Boot time; Shift B, measure each boot; "
			"D, details; M, settings and commands; U, undo changes; H, help. "
			"Every command can be reassigned in NVDA Input Gestures."
		)
