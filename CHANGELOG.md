# Changelog

## 1.3.2 — 2026-09-01

- Restored NVDA's native MSAA handling for the standard Autorun Organizer popup menu. The add-on had incorrectly forced UI Automation on the menu window, which made **Disable/Wyłącz** intermittently disappear or lose its checked state.
- Removed the 1.3.1 caption-based state workaround. Context-menu roles and states now come unchanged from the application's working MSAA provider; the add-on only translates the exposed caption.

## 1.3.1 — 2026-08-27

- Fixed the classic startup-item context menu: **Disable/Wyłącz** and other stateful commands now include their real checked state in the accessible label, including when Autorun Organizer exposes the menu through VCL/MSAA instead of UI Automation.
- Preserved the provider's native NVDA states and report **selection state unavailable** when Autorun Organizer does not expose a check state, instead of guessing.

## 1.3.0 — 2026-08-24

- Added a dedicated **Autorun Organizer Access** category to NVDA Settings.
- Added an independent spoken/braille language setting: follow Windows (default), English, Polish, or follow Autorun Organizer. Unsupported Windows and application languages fall back to English.
- Added Polish add-on messages, Input Gestures descriptions, documentation, and extensive translation of application captions exposed to NVDA through UI Automation or MSAA.
- Replaced inaccessible Sciter check boxes with accurately named action buttons. Autorun Organizer 6.x does not expose their current state, so NVDA no longer announces the misleading default state "unchecked".
- Added bidirectional accessible-name translation so changing between English and Polish does not leave stale translated captions.

## 1.2.0 — 2026-08-24

- Commands are now provided by an application-scoped global plug-in, so all of them are always visible in NVDA's Input Gestures dialog while their keys remain inactive outside Autorun Organizer 6.x.
- Expanded classic 6.x support for startup locations, selected-item commands, notification center, Settings and commands, Undo changes, status-bar actions, boot measurement controls, clickable labels, and startup-type radio buttons.
- Improved current-tab detail reporting and visibility filtering.
- Increased the remappable command set from 11 to 22 commands.
- Removed the Polish localization and Polish documentation; the package is now English-only.

## 1.1.0 — 2026-08-23

- Initial public release.
- Accessibility labels for the startup list and search field.
- Keyboard-operable overlays for Sciter filters, tabs, and toggles.
- Eleven remappable commands in NVDA's Input Gestures dialog.
- English interface messages and Polish translation.
- Support and tests for Autorun Organizer 6.32 and NVDA 2026.1.1.
