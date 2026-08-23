"""Unit tests for Autorun Organizer Access."""

import importlib.util
import builtins
import sys
import types
import unittest
from enum import Enum, auto
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "addon" / "appModules" / "autorunorganizer.py"


class Role(Enum):
	CHECKBOX = auto()
	TABCONTROL = auto()
	LIST = auto()
	LISTITEM = auto()
	BUTTON = auto()


class UIA:
	pass


class BaseAppModule:
	def __init__(self, *args, **kwargs):
		pass


class DummyLog:
	def debugWarning(self, *args, **kwargs):
		pass

	def error(self, *args, **kwargs):
		pass


def script(**metadata):
	def decorate(function):
		function.scriptMetadata = metadata
		return function
	return decorate


def load_module():
	stubs = {
		"addonHandler": types.SimpleNamespace(initTranslation=lambda: setattr(builtins, "_", lambda text: text)),
		"appModuleHandler": types.SimpleNamespace(AppModule=BaseAppModule),
		"api": types.SimpleNamespace(getForegroundObject=lambda: None, getFocusObject=lambda: None),
		"controlTypes": types.SimpleNamespace(Role=Role),
		"core": types.SimpleNamespace(callLater=lambda delay, function, *args: function(*args)),
		"mouseHandler": types.SimpleNamespace(doPrimaryClick=lambda: None),
		"ui": types.SimpleNamespace(message=lambda text: None),
		"winUser": types.SimpleNamespace(
			getCursorPos=lambda: (10, 20),
			setCursorPos=lambda x, y: None,
		),
		"logHandler": types.SimpleNamespace(log=DummyLog()),
		"scriptHandler": types.SimpleNamespace(script=script),
	}
	for name, module in stubs.items():
		sys.modules[name] = module
	nvda_objects = types.ModuleType("NVDAObjects")
	uia_module = types.ModuleType("NVDAObjects.UIA")
	uia_module.UIA = UIA
	sys.modules["NVDAObjects"] = nvda_objects
	sys.modules["NVDAObjects.UIA"] = uia_module
	spec = importlib.util.spec_from_file_location("autorunorganizer_under_test", MODULE_PATH)
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	return module


class DummyElement:
	def __init__(self, class_name):
		self.CurrentClassName = class_name


class DummyObject(UIA):
	def __init__(self, class_name, parent_name="", name="", role=None):
		self.UIAElement = DummyElement(class_name)
		self.parent = types.SimpleNamespace(name=parent_name)
		self.name = name
		self.role = role


class AppModuleTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.module = load_module()

	def setUp(self):
		self.app = object.__new__(self.module.AppModule)
		self.app._topFilterIndex = 0
		self.app._detailTabIndex = 1

	def test_sciter_overlays_are_selected_by_uia_and_parent_class(self):
		cases = {
			"Notifications": self.module._SciterToggle,
			"ToggleSwitcher2Holder": self.module._SciterToggle,
			"TopButtonsBarPanel": self.module._TopFilterSelector,
			"InfoPanelButtonsBarPanel": self.module._DetailTabSelector,
		}
		for parent_name, expected in cases.items():
			with self.subTest(parent_name=parent_name):
				classes = []
				obj = DummyObject("TSciterHostWindow", parent_name=parent_name)
				self.app.chooseNVDAObjectOverlayClasses(obj, classes)
				self.assertEqual(classes[0], expected)

	def test_shared_hwnd_class_does_not_affect_detection(self):
		classes = []
		obj = DummyObject("TButtonedEdit", name="")
		obj.windowClassName = "TAutorunOrganizerMainForm"
		self.app.event_NVDAObject_init(obj)
		self.assertEqual(obj.name, "Search startup items")

	def test_list_is_named(self):
		obj = DummyObject("TListView", name="", role=Role.LIST)
		self.app.event_NVDAObject_init(obj)
		self.assertEqual(obj.name, "Startup items")

	def test_filter_selector_cycles(self):
		selector = object.__new__(self.module._TopFilterSelector)
		selector.appModule = self.app
		selector._move(1)
		self.assertEqual(self.app._topFilterIndex, 1)
		self.assertIn("All", selector._get_name())

	def test_click_uses_relative_center(self):
		positions = []
		self.module.winUser.setCursorPos = lambda x, y: positions.append((x, y))
		obj = types.SimpleNamespace(location=(100, 200, 80, 40))
		self.assertTrue(self.app._clickObject(obj, xRatio=0.25))
		self.assertEqual(positions[0], (120, 220))
		self.assertEqual(positions[-1], (10, 20))

	def test_all_addon_commands_are_exposed_for_input_gesture_remapping(self):
		command_names = (
			"focusStartupList",
			"focusSearch",
			"viewImportant",
			"viewAll",
			"viewCustom",
			"toggleNotifications",
			"toggleStartupItem",
			"bootTimeTab",
			"applicationTab",
			"readDetails",
			"addonHelp",
		)
		self.assertEqual(self.module.AppModule.scriptCategory, "Autorun Organizer")
		gestures = []
		for name in command_names:
			with self.subTest(command=name):
				metadata = getattr(self.module.AppModule, f"script_{name}").scriptMetadata
				self.assertTrue(metadata.get("description"))
				self.assertTrue(metadata.get("gesture"))
				gestures.append(metadata["gesture"])
		self.assertEqual(len(gestures), len(set(gestures)))


if __name__ == "__main__":
	unittest.main()
