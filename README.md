# Autorun Organizer Access

An NVDA add-on that improves keyboard access to the classic Autorun Organizer 6.x interface.

The add-on was developed and tested with Autorun Organizer 6.32 and NVDA 2026.1.1. Autorun Organizer 7.0 uses a different, Sciter-rendered application list and is not supported by this release.

## Features

- Names the startup item list and search field exposed through UI Automation.
- Turns otherwise unnamed Sciter panels into keyboard-operable filters, tabs, and toggles.
- Adds direct commands for the startup list, search, view filters, item state, notifications, and detail tabs.
- Exposes every add-on command in NVDA's Input Gestures dialog.
- Includes English messages and a complete Polish translation.

## Installation

Download the `.nvda-addon` file from the latest GitHub release, open it while NVDA is running, confirm the installation, and restart NVDA.

## Commands

| Gesture | Action |
| --- | --- |
| NVDA+Alt+L | Focus the startup item list |
| NVDA+Alt+F | Focus search |
| NVDA+Alt+1 | Select the Important view |
| NVDA+Alt+2 | Select the All view |
| NVDA+Alt+3 | Select the Custom view |
| NVDA+Alt+S | Toggle the selected startup item |
| NVDA+Alt+N | Toggle Autorun Organizer notifications |
| NVDA+Alt+A | Open the Application tab |
| NVDA+Alt+B | Open the Boot time tab |
| NVDA+Alt+D | Read available details for the selected item |
| NVDA+Alt+H | Report add-on commands |

To change or remove a gesture, open **NVDA menu → Preferences → Input Gestures → Autorun Organizer**.

Arrow keys select an option when focus is on a virtual filter or details-tab control. Enter and Space activate the selected option or toggle.

## Compatibility and limitations

The Sciter controls used by Autorun Organizer 6.x do not expose their internal elements through UI Automation. The add-on activates these controls using positions relative to each control's current rectangle. This avoids fixed screen coordinates but can still be affected by major interface changes.

This project does not bundle Autorun Organizer and is not affiliated with ChemTable Software.

## Building and testing

Requirements:

- Windows PowerShell 5.1 or newer;
- Python 3.13 for unit tests;
- optional GNU `msgfmt` when recompiling the Polish translation.

Run:

```powershell
.\test.ps1
```

The release package is written to `dist`.

## License

Copyright © 2026 Patryk (Pates2004).

This add-on is distributed under the GNU General Public License version 2 or, at your option, any later version. See [COPYING.txt](COPYING.txt).
