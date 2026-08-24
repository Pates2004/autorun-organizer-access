# Autorun Organizer Access

An English-only NVDA add-on providing complete keyboard access to the classic Autorun Organizer 6.x interface.

The add-on targets the entire classic 6.x family and has been tested directly with Autorun Organizer 6.32 and NVDA 2026.1.1. Autorun Organizer 7.x uses a redesigned Sciter application list and is intentionally rejected by this add-on.

## Features

- Names the startup list, search field, status bar, top icon buttons, and status actions.
- Turns inaccessible Sciter filters, detail tabs, and switches into keyboard-operable NVDA controls.
- Makes clickable VCL labels and startup-type group buttons operable with Enter and Space.
- Provides direct access to all areas of the classic main window: startup filters and locations, selected-entry commands, notification settings and center, boot-time controls, application details, Settings and commands, background functions, reviews, and Undo changes.
- Exposes 22 commands permanently in NVDA's Input Gestures dialog. Assigned keys only become active while Autorun Organizer 6.x has focus, so they do not shadow shortcuts in other applications.
- Keeps destructive actions behind Autorun Organizer's own menus and confirmation dialogs.

The selected-entry command opens the application's standard context menu. From there, all actions supported for that entry remain available, including launch, open containing folder or startup location, search online, disable, delay, prevent re-enabling or undelaying, remove, uninstall, and additional properties. The exact entries depend on the selected startup item type.

## Installation

Download the `.nvda-addon` file from the latest GitHub release, open it while NVDA is running, confirm the installation, and restart NVDA.

## Commands

| Default gesture | Action |
| --- | --- |
| NVDA+Alt+L | Focus the startup item list |
| NVDA+Alt+F | Focus search |
| NVDA+Alt+1 | Select the Important view |
| NVDA+Alt+2 | Select the All view |
| NVDA+Alt+3 | Select the Custom view |
| NVDA+Alt+4 | Open the startup locations menu |
| NVDA+Alt+S | Enable or disable the selected startup item |
| NVDA+Alt+C | Open commands for the selected startup item |
| NVDA+Alt+N | Toggle notifications about new startup items |
| NVDA+Alt+Shift+N | Open the notification center |
| NVDA+Alt+A | Open the Application tab |
| NVDA+Alt+B | Open the Boot time tab |
| NVDA+Alt+Shift+B | Toggle measuring every system load time |
| NVDA+Alt+D | Read the selected item and current-tab details |
| NVDA+Alt+M | Open Settings and commands |
| NVDA+Alt+U | Open Undo changes |
| NVDA+Alt+H | Report the default commands |
| Unassigned | Open reviews |
| Unassigned | Toggle the interface theme |
| Unassigned | Open Background functions |
| Unassigned | Focus Reboot and measure |
| Unassigned | Focus the disable and delay frequency button |

All 22 commands are always listed under **NVDA menu → Preferences → Input Gestures → Autorun Organizer Access**, even when Autorun Organizer is not the currently focused application. Every default gesture can be changed or removed, and a gesture can be assigned to any command marked Unassigned.

When focus is on a virtual filter or details-tab control, use the arrow keys to choose an option and Enter or Space to activate it. Enter and Space also activate the virtual switches, clickable labels, group buttons, and newly labeled icon controls.

## Compatibility and limitations

Autorun Organizer 6.x renders several controls with Sciter without exposing their internal elements through UI Automation. The add-on activates those elements using positions relative to the current control rectangle rather than fixed screen coordinates. It also classifies the stable VCL panels by their parent, size, and relative position. This covers the classic 6.x layout across window positions and DPI settings, although a vendor redesign can require an add-on update.

Only 6.32 has been directly regression-tested. The add-on accepts all 6.x product versions because they use the classic control layout, but it refuses to apply its overlays and commands to 7.x.

This project does not bundle Autorun Organizer and is not affiliated with ChemTable Software.

## Building and testing

Requirements:

- Windows PowerShell 5.1 or newer;
- Python 3.13 for unit tests.

Run:

```powershell
.\test.ps1
```

The release package is written to `dist`.

## License

Copyright © 2026 Patryk (Pates2004).

This add-on is distributed under the GNU General Public License version 2 or, at your option, any later version. See [COPYING.txt](COPYING.txt).
