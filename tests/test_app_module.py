"""Unit tests for the Autorun Organizer 6.x app module."""

import importlib.util
import sys
import types
import unittest
from enum import Enum, auto
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "addon" / "appModules" / "autorunorganizer.py"
SHARED_PATH = Path(__file__).parents[1] / "addon" / "autorunOrganizerAccessShared.py"


class Role(Enum):
	CHECKBOX = auto()
	MENUITEM = auto()
	CHECKMENUITEM = auto()
	RADIOMENUITEM = auto()
	TABCONTROL = auto()
	LIST = auto()
	LISTITEM = auto()
	BUTTON = auto()
	RADIOBUTTON = auto()


class State(Enum):
	CHECKED = auto()
	HALFCHECKED = auto()
	CHECKABLE = auto()
	UNAVAILABLE = auto()


class UIA:
	pass


class BaseAppModule:
	appName = "autorunorganizer"
	productVersion = "6.32"

	def __init__(self, *args, **kwargs):
		pass


class DummyLog:
	def debugWarning(self, *args, **kwargs):
		pass

	def error(self, *args, **kwargs):
		pass


class DummyKeyboardGesture:
	sent = []

	@classmethod
	def fromName(cls, name):
		return types.SimpleNamespace(send=lambda: cls.sent.append(name))


FOCUS = {"foreground": None, "focus": None, "navigator": None}


def load_module():
	sharedSpec = importlib.util.spec_from_file_location("autorun_shared_for_app_tests", SHARED_PATH)
	shared = importlib.util.module_from_spec(sharedSpec)
	sharedSpec.loader.exec_module(shared)
	stubs = {
		"addonHandler": types.SimpleNamespace(
			getCodeAddon=lambda: types.SimpleNamespace(loadModule=lambda name: shared),
		),
		"appModuleHandler": types.SimpleNamespace(AppModule=BaseAppModule),
		"api": types.SimpleNamespace(
			getForegroundObject=lambda: FOCUS["foreground"],
			getFocusObject=lambda: FOCUS["focus"],
			setNavigatorObject=lambda obj: FOCUS.__setitem__("navigator", obj),
		),
		"controlTypes": types.SimpleNamespace(Role=Role, State=State),
		"core": types.SimpleNamespace(callLater=lambda delay, function, *args: function(*args)),
		"keyboardHandler": types.SimpleNamespace(KeyboardInputGesture=DummyKeyboardGesture),
		"mouseHandler": types.SimpleNamespace(doPrimaryClick=lambda: None),
		"ui": types.SimpleNamespace(message=lambda text: None),
		"winUser": types.SimpleNamespace(
			getCursorPos=lambda: (10, 20),
			getClassName=lambda hwnd: "#32768" if hwnd == 32768 else "TAutorunOrganizerMainForm",
			setCursorPos=lambda x, y: None,
			isWindowVisible=lambda hwnd: True,
		),
		"logHandler": types.SimpleNamespace(log=DummyLog()),
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
		self.CurrentIsOffscreen = False
		self.CurrentNativeWindowHandle = 0
		self.CurrentToggleState = None


class DummyObject(UIA):
	def __init__(
		self,
		class_name,
		*,
		parent=None,
		name="",
		role=None,
		location=(0, 0, 100, 30),
		children=None,
		states=None,
		checked=None,
	):
		self.UIAElement = DummyElement(class_name)
		self.parent = parent or types.SimpleNamespace(name="")
		self.name = name
		self.role = role
		self.location = location
		self.children = list(children or [])
		self.states = set(states or ())
		if checked is not None:
			self.checked = checked
		self.focused = False

	def _get_name(self):
		return self.name

	def _get_states(self):
		return set(self.states)

	def setFocus(self):
		self.focused = True


class AppModuleTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.module = load_module()

	def setUp(self):
		self.app = object.__new__(self.module.AppModule)
		self.app._topFilterIndex = 0
		self.app._detailTabIndex = 1
		DummyKeyboardGesture.sent.clear()
		FOCUS.update(foreground=None, focus=None, navigator=None)

	def test_sciter_overlays_cover_all_classic_6x_hosts(self):
		cases = {
			"Notifications": self.module._SciterActionButton,
			"ToggleSwitcher2Holder": self.module._SciterActionButton,
			"Measure each system load time": self.module._SciterActionButton,
			"TopButtonsBarPanel": self.module._TopFilterSelector,
			"InfoPanelButtonsBarPanel": self.module._DetailTabSelector,
		}
		for parent_name, expected in cases.items():
			with self.subTest(parent_name=parent_name):
				classes = []
				parent = DummyObject("TPanel", name=parent_name)
				obj = DummyObject("TSciterHostWindow", parent=parent)
				self.app.chooseNVDAObjectOverlayClasses(obj, classes)
				self.assertEqual(classes[0], expected)

	def test_sciter_switch_is_an_action_button_without_a_false_checked_state(self):
		parent = DummyObject("TPanel", name="ToggleSwitcher2Holder")
		obj = DummyObject("TSciterHostWindow", parent=parent)
		classes = []
		self.app.chooseNVDAObjectOverlayClasses(obj, classes)
		overlay = object.__new__(classes[0])
		overlay.parent = parent
		self.assertEqual(overlay._get_role(), Role.BUTTON)
		self.assertEqual(overlay._get_name(), "Enable or disable the selected startup item")

	def test_clickable_labels_and_group_buttons_are_keyboard_operable(self):
		cases = {
			"TClickableLabelControl": self.module._NativeClickableLabel,
			"TGroupButton": self.module._GroupButton,
		}
		for class_name, expected in cases.items():
			with self.subTest(class_name=class_name):
				classes = []
				self.app.chooseNVDAObjectOverlayClasses(DummyObject(class_name), classes)
				self.assertEqual(classes[0], expected)

	def test_top_icons_and_status_actions_receive_stable_names(self):
		top_parent = DummyObject("TStackPanel", location=(100, 0, 200, 40))
		top_cases = (
			(DummyObject("TPanel", parent=top_parent, location=(240, 5, 27, 30)), "Notification center"),
			(DummyObject("TPanel", parent=top_parent, location=(272, 5, 27, 30)), "Settings and commands"),
		)
		status_parent = DummyObject("TStatusBar", location=(0, 0, 735, 23))
		status_cases = (
			(DummyObject("TPanel", parent=status_parent, location=(422, 1, 20, 19)), "Interface theme"),
			(DummyObject("TPanel", parent=status_parent, location=(447, 1, 20, 19)), "Background functions"),
			(DummyObject("TPanel", parent=status_parent, location=(472, 1, 118, 19)), "Reviews"),
			(DummyObject("TPanel", parent=status_parent, location=(595, 1, 128, 19)), "Undo changes"),
		)
		for obj, name in top_cases + status_cases:
			with self.subTest(name=name):
				classes = []
				self.app.chooseNVDAObjectOverlayClasses(obj, classes)
				overlay = object.__new__(classes[0])
				overlay.UIAElement = obj.UIAElement
				overlay.parent = obj.parent
				overlay.location = obj.location
				self.assertEqual(overlay._get_name(), name)

	def test_main_window_controls_are_named(self):
		main_form = DummyObject("TAutorunOrganizerMainForm")
		startup_frame = DummyObject("TStartupManagerFrame", parent=main_form)
		cases = (
			(DummyObject("TButtonedEdit", parent=startup_frame), "Search startup items"),
			(DummyObject("TListView", parent=startup_frame, role=Role.LIST), "Startup items"),
			(DummyObject("TStatusBar", parent=main_form), "Autorun Organizer status"),
		)
		for obj, expected in cases:
			with self.subTest(expected=expected):
				self.app.event_NVDAObject_init(obj)
				self.assertEqual(obj.name, expected)

	def test_secondary_6x_forms_receive_contextual_control_names(self):
		settings = DummyObject("TSettingsForm")
		undo = DummyObject("TUndoingChangesCenterForm")
		new_item = DummyObject("TNewStartupItemForm")
		cases = (
			(DummyObject("TTreeView", parent=settings), "Settings categories"),
			(DummyObject("TControlList", parent=undo), "Changes that can be undone"),
			(DummyObject("TTreeView", parent=undo), "Objects affected by the selected change"),
			(DummyObject("TPageControl", parent=new_item), "Startup entry type"),
		)
		for obj, expected in cases:
			with self.subTest(expected=expected):
				self.app.event_NVDAObject_init(obj)
				self.assertEqual(obj.name, expected)

	def test_non_main_list_is_not_mislabeled_as_startup_items(self):
		obj = DummyObject("TListView", parent=DummyObject("TSettingsForm"), role=Role.LIST)
		self.app.event_NVDAObject_init(obj)
		self.assertEqual(obj.name, "")

	def test_standard_popup_menu_uses_native_msaa_provider(self):
		self.assertFalse(self.app.isGoodUIAWindow(32768))
		self.assertTrue(self.app.isBadUIAWindow(32768))
		self.assertTrue(self.app.isGoodUIAWindow(1))
		self.assertFalse(self.app.isBadUIAWindow(1))

	def test_context_menu_translation_preserves_native_checked_states(self):
		obj = DummyObject(
			"",
			name="Disable",
			role=Role.MENUITEM,
			states={State.CHECKABLE, State.CHECKED},
		)
		originalResolver = self.module._shared.resolveLanguage
		self.module._shared.resolveLanguage = lambda *args, **kwargs: "pl"
		try:
			self.app.event_NVDAObject_init(obj)
		finally:
			self.module._shared.resolveLanguage = originalResolver
		self.assertEqual(obj.name, "Wyłącz")
		self.assertEqual(obj.states, {State.CHECKABLE, State.CHECKED})
		self.assertEqual(obj.role, Role.MENUITEM)

	def test_filter_selector_cycles(self):
		selector = object.__new__(self.module._TopFilterSelector)
		selector.appModule = self.app
		selector._move(1)
		self.assertEqual(self.app._topFilterIndex, 1)
		self.assertIn("All", selector._get_name())

	def test_click_uses_relative_position_and_restores_mouse(self):
		positions = []
		self.module.winUser.setCursorPos = lambda x, y: positions.append((x, y))
		obj = types.SimpleNamespace(location=(100, 200, 80, 40))
		self.assertTrue(self.app._clickObject(obj, xRatio=0.25))
		self.assertEqual(positions[0], (120, 220))
		self.assertEqual(positions[-1], (10, 20))

	def test_selected_item_menu_uses_standard_context_menu_key(self):
		FOCUS["focus"] = types.SimpleNamespace(role=Role.LISTITEM)
		self.app.openSelectedItemMenu()
		self.assertEqual(DummyKeyboardGesture.sent, ["shift+f10"])

	def test_version_7_does_not_receive_classic_overlays(self):
		self.app.productVersion = "7.0"
		classes = []
		parent = DummyObject("TPanel", name="TopButtonsBarPanel")
		self.app.chooseNVDAObjectOverlayClasses(DummyObject("TSciterHostWindow", parent=parent), classes)
		self.assertEqual(classes, [])

	def test_app_module_does_not_duplicate_global_input_commands(self):
		self.assertFalse(any(name.startswith("script_") for name in self.module.AppModule.__dict__))


if __name__ == "__main__":
	unittest.main()
