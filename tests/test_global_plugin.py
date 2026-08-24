"""Tests for globally discoverable, application-scoped commands."""

import ast
import importlib.util
import sys
import types
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "addon" / "globalPlugins" / "autorunOrganizerAccess.py"
APP_MODULE_PATH = Path(__file__).parents[1] / "addon" / "appModules" / "autorunorganizer.py"
FOCUS = {"object": None}
MESSAGES = []


class BaseGlobalPlugin:
	def getScript(self, gesture):
		return getattr(self, f"script_{gesture.scriptName}", None)

	def terminate(self):
		pass


def script(*, description="", category=None, gesture=None, gestures=None, **kwargs):
	def decorate(function):
		function.__doc__ = description
		function.category = category
		assigned = list(gestures or [])
		if gesture:
			assigned.append(gesture)
		if assigned:
			function.gestures = assigned
		return function

	return decorate


def load_module():
	settingsPanels = []
	shared = types.SimpleNamespace(
		CONFIG_SECTION="autorunOrganizerAccess",
		LANGUAGE_MODES=("system", "en", "pl", "application"),
		registerConfig=lambda: None,
		resolveLanguage=lambda: "en",
		getConfiguredMode=lambda: "system",
		languageModeLabels=lambda language=None: (
			"Follow the Windows display language (default)",
			"English",
			"Polish",
			"Follow the Autorun Organizer language",
		),
		tr=lambda text, language=None, **kwargs: text.format(**kwargs) if kwargs else text,
	)
	configConf = {
		"autorunOrganizerAccess": {"language": "system"},
	}
	stubs = {
		"addonHandler": types.SimpleNamespace(
			getCodeAddon=lambda: types.SimpleNamespace(loadModule=lambda name: shared),
		),
		"api": types.SimpleNamespace(getFocusObject=lambda: FOCUS["object"]),
		"config": types.SimpleNamespace(conf=configConf),
		"globalPluginHandler": types.SimpleNamespace(GlobalPlugin=BaseGlobalPlugin),
		"gui": types.SimpleNamespace(
			settingsDialogs=types.SimpleNamespace(
				SettingsPanel=object,
				NVDASettingsDialog=types.SimpleNamespace(categoryClasses=settingsPanels),
			),
			guiHelper=types.SimpleNamespace(BoxSizerHelper=object),
		),
		"ui": types.SimpleNamespace(message=MESSAGES.append),
		"wx": types.SimpleNamespace(Choice=object, StaticText=object),
		"scriptHandler": types.SimpleNamespace(script=script),
	}
	for name, module in stubs.items():
		sys.modules[name] = module
	spec = importlib.util.spec_from_file_location("autorun_global_under_test", MODULE_PATH)
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	module._testSettingsPanels = settingsPanels
	return module


class Gesture:
	def __init__(self, scriptName):
		self.scriptName = scriptName


class FakeAppModule:
	appName = "autorunorganizer"
	isSupportedVersion = True

	def __init__(self):
		self.calls = []

	def focusStartupList(self):
		self.calls.append("focusStartupList")


class GlobalPluginTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.module = load_module()

	def setUp(self):
		FOCUS["object"] = None
		MESSAGES.clear()
		self.plugin = self.module.GlobalPlugin()

	def test_all_commands_are_globally_exposed_for_input_gestures(self):
		command_names = (
			"focusStartupList",
			"focusSearch",
			"viewImportant",
			"viewAll",
			"viewCustom",
			"openStartupLocations",
			"toggleStartupItem",
			"openSelectedItemMenu",
			"toggleNotifications",
			"openNotificationCenter",
			"bootTimeTab",
			"applicationTab",
			"toggleMeasureEachBoot",
			"readDetails",
			"openMainMenu",
			"openUndoChanges",
			"openReviews",
			"toggleTheme",
			"openBackgroundFunctions",
			"focusRebootAndMeasure",
			"focusFrequencyDisplay",
			"addonHelp",
		)
		gestures = []
		for name in command_names:
			with self.subTest(command=name):
				command = getattr(self.module.GlobalPlugin, f"script_{name}")
				self.assertTrue(command.__doc__)
				self.assertEqual(command.category, self.module.SCRIPT_CATEGORY)
				gestures.extend(getattr(command, "gestures", []))
		self.assertEqual(len(gestures), len(set(gestures)))
		self.assertEqual(self.module.GlobalPlugin.scriptCategory, "Autorun Organizer Access")

	def test_language_panel_is_registered_in_nvda_settings(self):
		self.assertIn(self.module.AutorunOrganizerAccessSettingsPanel, self.module._testSettingsPanels)

	def test_commands_do_not_shadow_keys_outside_autorun_organizer_6x(self):
		FOCUS["object"] = types.SimpleNamespace(
			appModule=types.SimpleNamespace(appName="notepad", isSupportedVersion=False),
		)
		self.assertIsNone(self.plugin.getScript(Gesture("focusStartupList")))

	def test_commands_are_active_and_routed_inside_autorun_organizer_6x(self):
		app = FakeAppModule()
		FOCUS["object"] = types.SimpleNamespace(appModule=app)
		command = self.plugin.getScript(Gesture("focusStartupList"))
		self.assertIsNotNone(command)
		command(None)
		self.assertEqual(app.calls, ["focusStartupList"])

	def test_version_7_is_rejected(self):
		FOCUS["object"] = types.SimpleNamespace(
			appModule=types.SimpleNamespace(appName="autorunorganizer", isSupportedVersion=False),
		)
		self.assertIsNone(self.plugin.getScript(Gesture("focusStartupList")))

	def test_every_routed_global_command_exists_in_the_app_module(self):
		globalTree = ast.parse(MODULE_PATH.read_text(encoding="utf-8"))
		appTree = ast.parse(APP_MODULE_PATH.read_text(encoding="utf-8"))
		routedMethods = {
			call.args[0].value
			for call in ast.walk(globalTree)
			if isinstance(call, ast.Call)
			and isinstance(call.func, ast.Attribute)
			and call.func.attr == "_callApp"
			and call.args
			and isinstance(call.args[0], ast.Constant)
			and isinstance(call.args[0].value, str)
		}
		appMethods = {
			node.name
			for node in ast.walk(appTree)
			if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
		}
		self.assertTrue(routedMethods)
		self.assertEqual(routedMethods - appMethods, set())


if __name__ == "__main__":
	unittest.main()
