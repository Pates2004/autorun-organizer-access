"""Unit tests for independent language selection and accessible UI translation."""

import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "addon" / "autorunOrganizerAccessShared.py"


def load_module():
	spec = importlib.util.spec_from_file_location("autorun_shared_under_test", MODULE_PATH)
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	return module


class SharedLanguageTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.module = load_module()

	def test_explicit_languages_override_everything(self):
		self.assertEqual(self.module.resolveLanguage("en", "pl_PL", "pl"), "en")
		self.assertEqual(self.module.resolveLanguage("pl", "en_US", "en"), "pl")

	def test_system_language_supports_polish_and_falls_back_to_english(self):
		self.assertEqual(self.module.resolveLanguage("system", "pl_PL"), "pl")
		self.assertEqual(self.module.resolveLanguage("system", "de_DE"), "en")

	def test_application_mode_uses_detected_supported_language(self):
		self.assertEqual(self.module.resolveLanguage("application", applicationLanguage="pl"), "pl")
		self.assertEqual(self.module.resolveLanguage("application", applicationLanguage="ru"), "en")

	def test_addon_messages_are_translated_and_formatted(self):
		self.assertEqual(self.module.tr("Startup items", language="pl"), "Elementy autostartu")
		self.assertEqual(
			self.module.tr("Selected: {label}", language="pl", label="Wszystkie"),
			"Wybrano: Wszystkie",
		)

	def test_application_text_is_translated_in_both_directions(self):
		self.assertEqual(self.module.translateApplicationText("Settings", "pl"), "Ustawienia")
		self.assertEqual(self.module.translateApplicationText("Ustawienia", "en"), "Settings")
		self.assertEqual(self.module.translateApplicationText("Reviews (70+)", "pl"), "Recenzje (70+)")
		self.assertEqual(
			self.module.translateApplicationText("Uninstall Example App", "pl"),
			"Odinstaluj Example App",
		)
		self.assertTrue(
			self.module.startsWithApplicationText("Uruchom ponownie i zmierz jeszcze raz", "Reboot and measure")
		)

	def test_language_mode_labels_cover_all_modes(self):
		self.assertEqual(len(self.module.languageModeLabels("pl")), len(self.module.LANGUAGE_MODES))
		self.assertIn("domyślnie", self.module.languageModeLabels("pl")[0])


if __name__ == "__main__":
	unittest.main()
