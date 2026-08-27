# -*- coding: utf-8 -*-
# Copyright (C) 2026 Patryk (Pates2004)
# SPDX-License-Identifier: GPL-2.0-or-later
"""Shared language and configuration support for Autorun Organizer Access."""

import re

CONFIG_SECTION = "autorunOrganizerAccess"
LANGUAGE_MODES = ("system", "en", "pl", "application")
CONFIG_SPEC = {
	"language": 'option("system", "en", "pl", "application", default="system")',
}


_POLISH = {
	# Settings.
	"Language used for add-on messages and Autorun Organizer text spoken by NVDA:": (
		"Język komunikatów dodatku i tekstów Autorun Organizer odczytywanych przez NVDA:"
	),
	"Follow the Windows display language (default)": "Zgodnie z językiem systemu Windows (domyślnie)",
	"English": "Angielski",
	"Polish": "Polski",
	"Follow the Autorun Organizer language": "Zgodnie z językiem Autorun Organizer",
	"Windows and application languages other than Polish use English. The setting changes what NVDA speaks and displays on a braille display; it does not change text drawn visually by Autorun Organizer.": (
		"Języki systemu Windows i programu inne niż polski używają angielskiego. Ustawienie zmienia tekst "
		"odczytywany przez NVDA i pokazywany na monitorze brajlowskim; nie zmienia napisów wyświetlanych "
		"wizualnie przez Autorun Organizer."
	),
	# Virtual controls and stable names.
	"Important": "Najważniejsze",
	"All": "Wszystkie",
	"Custom": "Niestandardowe",
	"Boot time": "Czas uruchamiania",
	"Application": "Aplikacja",
	"Notification center": "Centrum powiadomień",
	"Settings and commands": "Ustawienia i polecenia",
	"Interface theme": "Motyw interfejsu",
	"Background functions": "Funkcje w tle",
	"Reviews": "Recenzje",
	"Undo changes": "Cofnij zmiany",
	"Autorun Organizer action": "Działanie Autorun Organizer",
	"Autorun Organizer status action": "Działanie na pasku stanu Autorun Organizer",
	"Enable or disable notifications about new startup items": (
		"Włącz lub wyłącz powiadomienia o nowych elementach autostartu"
	),
	"Enable or disable measuring every system startup": (
		"Włącz lub wyłącz pomiar każdego uruchomienia systemu"
	),
	"Enable or disable the selected startup item": "Włącz lub wyłącz wybrany element autostartu",
	"Autorun Organizer switch": "Przełącznik Autorun Organizer",
	"Command sent. Autorun Organizer does not expose the resulting state to NVDA.": (
		"Polecenie wysłane. Autorun Organizer nie udostępnia NVDA stanu po przełączeniu."
	),
	"Unable to activate the control.": "Nie udało się uaktywnić kontrolki.",
	"{label}, {position} of {count}": "{label}, {position} z {count}",
	"Selected: {label}": "Wybrano: {label}",
	"Unable to select the item.": "Nie udało się wybrać elementu.",
	"View filter": "Filtr widoku",
	"Details tab": "Zakładka szczegółów",
	"Search startup items": "Szukaj elementów autostartu",
	"Startup items": "Elementy autostartu",
	"Autorun Organizer status": "Pasek stanu Autorun Organizer",
	"Settings categories": "Kategorie ustawień",
	"Objects affected by the selected change": "Obiekty objęte wybraną zmianą",
	"Changes that can be undone": "Zmiany, które można cofnąć",
	"Startup entry type": "Typ wpisu autostartu",
	# Context-menu state feedback.  These labels are included in the accessible
	# name so the state is spoken even when a VCL/MSAA menu item does not expose
	# a reliable CHECKED state to NVDA.
	"checked": "zaznaczone",
	"not checked": "niezaznaczone",
	"partially checked": "cz\u0119\u015bciowo zaznaczone",
	"selection state unavailable": "stan zaznaczenia niedost\u0119pny",
	"{name}; {state}": "{name}; {state}",
	# Runtime feedback.
	"This control is not currently available in the application window.": (
		"Ta kontrolka nie jest teraz dostępna w oknie programu."
	),
	"NVDA navigator object set": "Ustawiono obiekt nawigatora NVDA",
	"Unable to move focus.": "Nie udało się przenieść fokusu.",
	"{name} is not currently available.": "{name} nie jest teraz dostępne.",
	"Opened {name}.": "Otwarto: {name}.",
	"Activated {name}.": "Uaktywniono: {name}.",
	"View: {label}": "Widok: {label}",
	"Tab: {label}": "Zakładka: {label}",
	"Unable to send the keyboard command.": "Nie udało się wysłać polecenia klawiaturowego.",
	"The startup item list was not found.": "Nie znaleziono listy elementów autostartu.",
	"The search field was not found.": "Nie znaleziono pola wyszukiwania.",
	"Startup locations menu opened.": "Otwarto menu lokalizacji autostartu.",
	"Notification command sent. The resulting state is not exposed to NVDA.": (
		"Polecenie dotyczące powiadomień zostało wysłane. Stan po przełączeniu nie jest udostępniany NVDA."
	),
	"Startup item command sent. The resulting enabled or disabled state is not exposed to NVDA.": (
		"Polecenie dotyczące elementu autostartu zostało wysłane. Stan włączenia lub wyłączenia nie jest "
		"udostępniany NVDA."
	),
	"Measurement command sent. The resulting state is not exposed to NVDA.": (
		"Polecenie dotyczące pomiaru zostało wysłane. Stan po przełączeniu nie jest udostępniany NVDA."
	),
	"No details are available for the current item or tab.": (
		"Brak szczegółów dla bieżącego elementu lub zakładki."
	),
	"The {name} button was not found.": "Nie znaleziono przycisku {name}.",
	"The disable and delay frequency button was not found.": (
		"Nie znaleziono przycisku częstotliwości wyłączania i opóźniania."
	),
	"Autorun Organizer 6.x is not active.": "Autorun Organizer 6.x nie jest aktywny.",
	"This command is not available in the current Autorun Organizer window.": (
		"To polecenie nie jest dostępne w bieżącym oknie Autorun Organizer."
	),
	# Input Gestures descriptions.
	"Move focus to the startup item list": "Przenieś fokus do listy elementów autostartu",
	"Move focus to the search field": "Przenieś fokus do pola wyszukiwania",
	"Select the Important view": "Wybierz widok Najważniejsze",
	"Select the All view": "Wybierz widok Wszystkie",
	"Select the Custom view": "Wybierz widok Niestandardowe",
	"Open the startup locations menu": "Otwórz menu lokalizacji autostartu",
	"Open commands for the selected startup item": "Otwórz polecenia wybranego elementu autostartu",
	"Toggle notifications about new startup items": (
		"Włącz lub wyłącz powiadomienia o nowych elementach autostartu"
	),
	"Open the notification center": "Otwórz centrum powiadomień",
	"Open the Boot time tab": "Otwórz zakładkę Czas uruchamiania",
	"Open the Application tab": "Otwórz zakładkę Aplikacja",
	"Toggle measuring every system load time": "Włącz lub wyłącz pomiar każdego uruchomienia systemu",
	"Read details for the selected item or current details tab": (
		"Odczytaj szczegóły wybranego elementu lub bieżącej zakładki"
	),
	"Open Settings and commands": "Otwórz Ustawienia i polecenia",
	"Open Undo changes": "Otwórz Cofnij zmiany",
	"Open reviews": "Otwórz recenzje",
	"Toggle the Autorun Organizer interface theme": "Przełącz motyw interfejsu Autorun Organizer",
	"Open Background functions": "Otwórz Funkcje w tle",
	"Move focus to Reboot and measure": "Przenieś fokus do Uruchom ponownie i zmierz",
	"Move focus to disable and delay frequency": (
		"Przenieś fokus do częstotliwości wyłączania i opóźniania"
	),
	"Report Autorun Organizer Access commands": "Podaj polecenia Autorun Organizer Access",
	"Commands: NVDA plus Alt plus L, list; F, search; 1, 2, 3, filters; 4, startup locations; S, toggle item; C, item commands; N, notification toggle; Shift N, notification center; A, Application tab; B, Boot time; Shift B, measure each boot; D, details; M, settings and commands; U, undo changes; H, help. Every command can be reassigned in NVDA Input Gestures.": (
		"Polecenia: NVDA plus Alt plus L, lista; F, wyszukiwanie; 1, 2, 3, filtry; 4, lokalizacje "
		"autostartu; S, przełączenie elementu; C, polecenia elementu; N, przełączenie powiadomień; "
		"Shift N, centrum powiadomień; A, zakładka Aplikacja; B, Czas uruchamiania; Shift B, pomiar "
		"każdego uruchomienia; D, szczegóły; M, ustawienia i polecenia; U, cofanie zmian; H, pomoc. "
		"Każde polecenie można przypisać ponownie w Zdarzeniach wejścia NVDA."
	),
}


# Exact application captions exposed through UI Automation or MSAA. These
# translations only affect what NVDA speaks and displays in braille.
_APPLICATION_EN_TO_PL = {
	"Most Important": "Najważniejsze",
	"Important": "Najważniejsze",
	"All": "Wszystkie",
	"Custom": "Niestandardowe",
	"Notifications": "Powiadomienia",
	"Find": "Znajdź",
	"Search": "Wyszukaj",
	"Startup Application": "Aplikacja uruchamiana przy starcie",
	"Comment": "Komentarz",
	"Boot time": "Czas uruchamiania",
	"BOOT TIME": "CZAS URUCHAMIANIA",
	"Application": "Aplikacja",
	"APPLICATION": "APLIKACJA",
	"Description": "Opis",
	"File": "Plik",
	"File path": "Ścieżka pliku",
	"Command": "Polecenie",
	"Location": "Lokalizacja",
	"Publisher": "Wydawca",
	"Status": "Stan",
	"Enabled": "Włączony",
	"Disabled": "Wyłączony",
	"Delayed": "Opóźniony",
	"Not measured": "Nie zmierzono",
	"Reboot and measure": "Uruchom ponownie i zmierz",
	"Reboot and measure again": "Uruchom ponownie i zmierz jeszcze raz",
	"Measure each system load time": "Mierz czas każdego uruchomienia systemu",
	"Display": "Wyświetl",
	"Display which applications get disabled frequently?": (
		"Wyświetl aplikacje, które są często wyłączane"
	),
	"This requires sending the startup applications data to the server": (
		"Wymaga to wysłania na serwer danych o aplikacjach uruchamianych przy starcie"
	),
	"Online virus scan on VirusTotal disabled. Click to enable.": (
		"Skanowanie online w VirusTotal jest wyłączone. Kliknij, aby włączyć."
	),
	"Settings": "Ustawienia",
	"Settings and Commands": "Ustawienia i polecenia",
	"Settings and commands": "Ustawienia i polecenia",
	"Startup locations": "Lokalizacje autostartu",
	"Add to Startup": "Dodaj do autostartu",
	"Add a new startup item": "Dodaj nowy element autostartu",
	"Open": "Otwórz",
	"Run": "Uruchom",
	"Open containing folder": "Otwórz folder zawierający",
	"Open startup location": "Otwórz lokalizację autostartu",
	"Search online": "Wyszukaj w Internecie",
	"Enable": "Włącz",
	"Disable": "Wyłącz",
	"Delay Load": "Opóźnij uruchomienie",
	"Delay load": "Opóźnij uruchomienie",
	"Remove Delay": "Usuń opóźnienie",
	"Remove delay": "Usuń opóźnienie",
	"Prevent disabling": "Zapobiegaj wyłączeniu",
	"Prevent enabling": "Zapobiegaj włączeniu",
	"Prevent delaying": "Zapobiegaj opóźnieniu",
	"Prevent undelaying": "Zapobiegaj usunięciu opóźnienia",
	"Remove": "Usuń",
	"Uninstall": "Odinstaluj",
	"Properties": "Właściwości",
	"Additional properties": "Dodatkowe właściwości",
	"Refresh": "Odśwież",
	"Select all": "Zaznacz wszystko",
	"Undo Changes": "Cofnij zmiany",
	"Undo changes": "Cofnij zmiany",
	"Changes that can be undone": "Zmiany, które można cofnąć",
	"Undo": "Cofnij",
	"Restore": "Przywróć",
	"Delete": "Usuń",
	"Background functions": "Funkcje w tle",
	"Reviews": "Recenzje",
	"Interface theme": "Motyw interfejsu",
	"Notification center": "Centrum powiadomień",
	"Close": "Zamknij",
	"Cancel": "Anuluj",
	"OK": "OK",
	"Yes": "Tak",
	"No": "Nie",
	"Apply": "Zastosuj",
	"Help": "Pomoc",
	"General": "Ogólne",
	"Interface": "Interfejs",
	"Updates": "Aktualizacje",
	"Language": "Język",
	"Startup entry type": "Typ wpisu autostartu",
	"Registry": "Rejestr",
	"Task Scheduler": "Harmonogram zadań",
	"Startup Folder": "Folder Autostart",
	"Tasks Scheduler": "Harmonogram zadań",
	"Services": "Usługi",
	"Drivers": "Sterowniki",
	"COMMANDS": "POLECENIA",
	"STARTUP LOCATIONS": "LOKALIZACJE AUTOSTARTU",
	"Check All": "Zaznacz wszystko",
	"Uncheck All": "Odznacz wszystko",
	"Hide System Applications": "Ukryj aplikacje systemowe",
	"Show the Startup Entry Location": "Pokaż lokalizację wpisu autostartu",
	"Show the File Properties": "Pokaż właściwości pliku",
	"Open the Containing Folder": "Otwórz folder zawierający",
	"Launch": "Uruchom",
	"Mark as Recently Added/Old": "Oznacz jako ostatnio dodany lub stary",
	"Mark as Recently Added": "Oznacz jako ostatnio dodany",
	"Mark as Old": "Oznacz jako stary",
	"Mark All Items as Old": "Oznacz wszystkie elementy jako stare",
	"Hide the VirusTotal Status": "Ukryj stan VirusTotal",
	"Hide the Optimization Recommendation": "Ukryj zalecenie optymalizacji",
	"Prevent Re-Enabling": "Zapobiegaj ponownemu włączeniu",
	"Prevent Changing the Delay Time": "Zapobiegaj zmianie czasu opóźnienia",
	"Remove and Prevent Reappearance": "Usuń i zapobiegaj ponownemu pojawieniu",
	"Do Not Notify Me about Adding to the Startup": "Nie powiadamiaj o dodawaniu do autostartu",
	"Display the Applications' Disable/Delay Frequency": (
		"Wyświetl częstotliwość wyłączania i opóźniania aplikacji"
	),
	"Enable Startup Checking": "Włącz sprawdzanie autostartu",
	"VirusTotal Online Scan": "Skanowanie online VirusTotal",
	"Send Unknown Applications for Analysis": "Wysyłaj nieznane aplikacje do analizy",
	"Bulk Entries Changing": "Zbiorcza zmiana wpisów",
	"Clear the System Load Time List": "Wyczyść listę czasów uruchamiania systemu",
	"Delay Load for...": "Opóźnij uruchomienie o...",
	"Optimization Available...": "Dostępna optymalizacja...",
	"Undo Removal": "Cofnij usunięcie",
	"Uninstall Application": "Odinstaluj aplikację",
	"Return to normal mode": "Powróć do trybu normalnego",
	"Startup type": "Typ uruchamiania",
	"Show Details": "Pokaż szczegóły",
	"Cancel Delayed Load": "Anuluj opóźnione uruchomienie",
	"Number of seconds to delay this application’s load:": (
		"Liczba sekund opóźnienia uruchomienia tej aplikacji:"
	),
	"Making changes": "Wprowadzanie zmian",
	"This may take a few seconds...": "Może to potrwać kilka sekund...",
	"The load takes:": "Uruchamianie trwa:",
	"Disable/Delay Frequency": "Częstotliwość wyłączania i opóźniania",
	"Data to be sent to the server:": "Dane wysyłane na serwer:",
	"Performing the optimization.": "Trwa optymalizacja.",
	"The removal cannot be cancelled.": "Usunięcia nie można anulować.",
	"Online antivirus check of the application…": "Trwa skanowanie aplikacji przez antywirus online…",
	"The application will be submitted to the server for analysis...": (
		"Aplikacja zostanie wysłana na serwer do analizy..."
	),
	"The application has been submitted for analysis. It may take a while...": (
		"Aplikacja została wysłana do analizy. Może to potrwać..."
	),
	"The removed entries can be restored at any time. Click here.": (
		"Usunięte wpisy można przywrócić w dowolnym momencie. Kliknij tutaj."
	),
	"Preparing the optimization plan.": "Przygotowywanie planu optymalizacji.",
	"The optimization can be cancelled through the Undo Changes Center.": (
		"Optymalizację można anulować w Centrum cofania zmian."
	),
	"This application has a high impact on the system startup.": (
		"Ta aplikacja ma duży wpływ na uruchamianie systemu."
	),
	"Quit the Bulk Entries Changing Mode": "Zakończ tryb zbiorczej zmiany wpisów",
	"New Startup Application": "Nowa aplikacja w autostarcie",
	"Status: Safe Application": "Stan: bezpieczna aplikacja",
	"Optimization is possible": "Optymalizacja jest możliwa",
	"Apply Optimization": "Zastosuj optymalizację",
	"Disable at Startup": "Wyłącz w autostarcie",
	"A SUSPICIOUS application was added to the startup!": (
		"Do autostartu dodano PODEJRZANĄ aplikację!"
	),
	"A new startup application was added.": "Dodano nową aplikację do autostartu.",
	"A new SAFE startup application was added.": "Dodano nową BEZPIECZNĄ aplikację do autostartu.",
	"A new startup application was added. It can be optimized!": (
		"Dodano nową aplikację do autostartu. Można ją zoptymalizować!"
	),
	"Remove Entry and Disable Startup Checking": "Usuń wpis i wyłącz sprawdzanie autostartu",
	"Remove Entry and Disable Functions": "Usuń wpis i wyłącz funkcje",
	"Prevent Undelay": "Zapobiegaj usunięciu opóźnienia",
	"This application cannot be changed": "Tej aplikacji nie można zmienić",
	"You will see the result here shortly": "Wkrótce pojawi się tutaj wynik",
	"All load times will be added there": "Zostaną tu dodane wszystkie czasy uruchamiania",
	"Measuring the current load time…": "Pomiar bieżącego czasu uruchamiania…",
	"The current load’s time was not measured": "Nie zmierzono czasu bieżącego uruchomienia",
	"The load time has not been measured yet": "Czas uruchamiania nie został jeszcze zmierzony",
	"Measuring the system load time": "Pomiar czasu uruchamiania systemu",
	"Your computer will now be rebooted.": "Komputer zostanie teraz uruchomiony ponownie.",
	"Done": "Gotowe",
	"Still measuring system load time...": "Pomiar czasu uruchamiania systemu nadal trwa...",
	"Click for the details.": "Kliknij, aby wyświetlić szczegóły.",
	"Current load": "Bieżące uruchomienie",
	"Time remaining": "Pozostały czas",
	"Perform Optimization": "Wykonaj optymalizację",
	"System Boot Optimization": "Optymalizacja uruchamiania systemu",
	"Blocked Applications": "Zablokowane aplikacje",
	"Restore the Application": "Przywróć aplikację",
	"old value": "stara wartość",
	"See More Details": "Pokaż więcej szczegółów",
	"Show Me How to Do It": "Pokaż, jak to zrobić",
	"NOTIFICATIONS": "POWIADOMIENIA",
	"Mark all as unread": "Oznacz wszystkie jako nieprzeczytane",
	"More Details": "Więcej szczegółów",
	"There are no notifications now.": "Obecnie nie ma powiadomień.",
	"Don't Show This Notification Anymore": "Nie pokazuj więcej tego powiadomienia",
	"Add a New Startup Entry": "Dodaj nowy wpis autostartu",
	"WHAT TO ADD TO STARTUP": "CO DODAĆ DO AUTOSTARTU",
	"Path:": "Ścieżka:",
	"Name:": "Nazwa:",
	"Specify the file path": "Podaj ścieżkę pliku",
	"ENTRY LOCATION": "LOKALIZACJA WPISU",
	"The entry will be created in": "Wpis zostanie utworzony w",
	"Forward >": "Dalej >",
	"< Back": "< Wstecz",
	"Finish": "Zakończ",
	"The program will be restarted to apply changes": (
		"Program zostanie uruchomiony ponownie w celu zastosowania zmian"
	),
	"Program interface language:": "Język interfejsu programu:",
	"Cleanup Ignore List": "Lista ignorowanych podczas czyszczenia",
	"Item": "Element",
	"Type": "Typ",
	"Add": "Dodaj",
	"Invalid Shortcuts": "Nieprawidłowe skróty",
	"Applications": "Aplikacje",
	"Windows context menu commands": "Polecenia menu kontekstowego Windows",
	"Custom Files": "Pliki niestandardowe",
	"Obsolete Tools": "Przestarzałe narzędzia",
	"Connection": "Połączenie",
	"Proxy server is:": "Serwer proxy:",
	"Change the proxy server settings": "Zmień ustawienia serwera proxy",
	"Proxy server requires authorization": "Serwer proxy wymaga uwierzytelnienia",
	"Authorization settings": "Ustawienia uwierzytelniania",
	"Username:": "Nazwa użytkownika:",
	"Password:": "Hasło:",
	"System Cleanup": "Czyszczenie systemu",
	"Disk Analyzer": "Analizator dysku",
	"Launch %s when the system starts": "Uruchamiaj %s podczas startu systemu",
	"Not yet performed": "Jeszcze nie wykonano",
	"Set up": "Skonfiguruj",
	"Reset the settings to the default values": "Przywróć ustawienia domyślne",
	"HELP": "POMOC",
	"User's Manual": "Podręcznik użytkownika",
	"Get Technical Support": "Uzyskaj pomoc techniczną",
	"Home Page": "Strona główna",
	"Settings...": "Ustawienia...",
	"Check For Updates...": "Sprawdź aktualizacje...",
	"Re-Show the Interface Hints": "Ponownie pokaż wskazówki interfejsu",
	"Undo Changes Center": "Centrum cofania zmian",
	"Show change details": "Pokaż szczegóły zmiany",
	"Title": "Tytuł",
	"Undo the Change": "Cofnij zmianę",
	"Delete item. The backup will not be restored.": (
		"Usuń element. Kopia zapasowa nie zostanie przywrócona."
	),
	"Undoing changes...": "Cofanie zmian...",
	"An error occurred.": "Wystąpił błąd.",
	"Error": "Błąd",
	"just now": "przed chwilą",
	"Hide change details": "Ukryj szczegóły zmiany",
	"Date": "Data",
	"This may take a minute": "Może to potrwać minutę",
	"Separate registry entries": "Oddzielne wpisy rejestru",
	"Registry Cleanup": "Czyszczenie rejestru",
	"Registry search results": "Wyniki wyszukiwania w rejestrze",
	"Open the folder": "Otwórz folder",
	"Open Recycle Bin": "Otwórz Kosz",
	"Preparing the data": "Przygotowywanie danych",
	"Please wait...": "Proszę czekać...",
	"System Restore point": "Punkt przywracania systemu",
	"Preparing for restore...": "Przygotowywanie do przywrócenia...",
	"Press ESC to cancel": "Naciśnij Escape, aby anulować",
	"This may take a while...": "Może to potrwać...",
}

_APPLICATION_PL_TO_EN = {polish.casefold(): english for english, polish in _APPLICATION_EN_TO_PL.items()}
_APPLICATION_EN_CASEFOLD = {english.casefold(): polish for english, polish in _APPLICATION_EN_TO_PL.items()}

_APPLICATION_EN_TO_PL_PATTERNS = (
	(r"^System load took (\d+) seconds$", r"Uruchamianie systemu trwało \1 s"),
	(r"^Delay Load for (\d+) Seconds$", r"Opóźnij uruchomienie o \1 s"),
	(r"^Delayed: (\d+) s\.$", r"Opóźniono o \1 s"),
	(r"^(\d+) seconds$", r"\1 sekund"),
	(r"^1 second$", "1 sekunda"),
	(r"^(\d+) minutes ago$", r"\1 minut temu"),
	(r"^(\d+) hours ago$", r"\1 godzin temu"),
	(r"^(\d+) days ago$", r"\1 dni temu"),
	(r"^Objects which will be affected on undoing this change \((\d+)\)$", r"Obiekty objęte cofnięciem tej zmiany (\1)"),
	(r"^And (\d+) more file\(s\)$", r"I jeszcze \1 plików"),
	(r"^(.+): Additional Properties$", r"\1: dodatkowe właściwości"),
	(r"^Removed Startup Application: (.+)$", r"Usunięta aplikacja autostartu: \1"),
	(r"^Startup item: (.+)$", r"Element autostartu: \1"),
)

_APPLICATION_PL_TO_EN_PATTERNS = (
	(r"^Uruchamianie systemu trwało (\d+) s$", r"System load took \1 seconds"),
	(r"^Opóźnij uruchomienie o (\d+) s$", r"Delay Load for \1 Seconds"),
	(r"^Opóźniono o (\d+) s$", r"Delayed: \1 s."),
	(r"^(\d+) sekund$", r"\1 seconds"),
	(r"^1 sekunda$", "1 second"),
)


def registerConfig():
	"""Register the add-on configuration section with NVDA."""
	import config

	if CONFIG_SECTION not in config.conf.spec:
		config.conf.spec[CONFIG_SECTION] = CONFIG_SPEC
	else:
		config.conf.spec[CONFIG_SECTION].update(CONFIG_SPEC)


def getConfiguredMode():
	try:
		registerConfig()
		import config

		mode = str(config.conf[CONFIG_SECTION]["language"])
	except Exception:
		mode = "system"
	return mode if mode in LANGUAGE_MODES else "system"


def getWindowsLanguage():
	try:
		import languageHandler

		return str(languageHandler.getWindowsLanguage() or "en")
	except Exception:
		return "en"


def getApplicationLanguage():
	"""Return the active Autorun Organizer language, limited to supported output languages."""
	try:
		import winreg

		with winreg.OpenKey(
			winreg.HKEY_CURRENT_USER,
			r"Software\ChemTable Software\Autorun Organizer\Translation",
		) as key:
			for valueName in ("Language", "LanguageSimulation"):
				try:
					value = str(winreg.QueryValueEx(key, valueName)[0]).strip().casefold()
				except OSError:
					continue
				if value in {"pl", "pl_pl", "polish", "polski", "polska"} or "polish" in value:
					return "pl"
				return "en"
	except OSError:
		pass
	# The built-in application language is English. External translations only
	# become active after the registry value above is created by the program.
	return "en"


def resolveLanguage(mode=None, windowsLanguage=None, applicationLanguage=None):
	"""Resolve a configured language mode to the supported language code en or pl."""
	mode = mode or getConfiguredMode()
	if mode == "pl":
		return "pl"
	if mode == "en":
		return "en"
	if mode == "application":
		language = applicationLanguage if applicationLanguage is not None else getApplicationLanguage()
	else:
		language = windowsLanguage if windowsLanguage is not None else getWindowsLanguage()
	language = str(language or "en").replace("-", "_").casefold()
	return "pl" if language == "pl" or language.startswith("pl_") else "en"


def tr(text, language=None, **formatArgs):
	"""Translate an add-on message using the independently configured language."""
	language = language or resolveLanguage()
	translated = _POLISH.get(text, text) if language == "pl" else text
	return translated.format(**formatArgs) if formatArgs else translated


def languageModeLabels(language=None):
	return (
		tr("Follow the Windows display language (default)", language=language),
		tr("English", language=language),
		tr("Polish", language=language),
		tr("Follow the Autorun Organizer language", language=language),
	)


def _translateApplicationFragment(fragment, language):
	leading = fragment[: len(fragment) - len(fragment.lstrip())]
	trailing = fragment[len(fragment.rstrip()) :]
	core = fragment.strip()
	if not core:
		return fragment
	shortcut = ""
	if "\t" in core:
		core, shortcut = core.split("\t", 1)
		shortcut = "\t" + shortcut
	lookup = core.replace("&", "").strip()
	if language == "pl":
		translated = _APPLICATION_EN_CASEFOLD.get(lookup.casefold())
		if translated is None:
			lower = lookup.casefold()
			if lower.startswith("uninstall "):
				translated = "Odinstaluj " + lookup[len("Uninstall ") :]
			elif lower.startswith("reviews ("):
				translated = "Recenzje " + lookup[len("Reviews ") :]
		if translated is None:
			for pattern, replacement in _APPLICATION_EN_TO_PL_PATTERNS:
				if re.match(pattern, lookup, flags=re.IGNORECASE):
					translated = re.sub(pattern, replacement, lookup, flags=re.IGNORECASE)
					break
	else:
		translated = _APPLICATION_PL_TO_EN.get(lookup.casefold())
		if translated is None:
			lower = lookup.casefold()
			if lower.startswith("odinstaluj "):
				translated = "Uninstall " + lookup[len("Odinstaluj ") :]
			elif lower.startswith("recenzje ("):
				translated = "Reviews " + lookup[len("Recenzje ") :]
		if translated is None:
			for pattern, replacement in _APPLICATION_PL_TO_EN_PATTERNS:
				if re.match(pattern, lookup, flags=re.IGNORECASE):
					translated = re.sub(pattern, replacement, lookup, flags=re.IGNORECASE)
					break
	return leading + (translated if translated is not None else core) + shortcut + trailing


def translateApplicationText(text, language=None):
	"""Translate application-provided accessible text in both directions."""
	if not isinstance(text, str) or not text:
		return text
	language = language or resolveLanguage()
	return "\n".join(_translateApplicationFragment(line, language) for line in text.split("\n"))


def matchesApplicationText(text, englishText):
	"""Match an accessible caption after either English or Polish relabeling."""
	value = str(text or "").replace("&", "").strip().casefold()
	polishText = _APPLICATION_EN_TO_PL.get(englishText, "")
	return value in {englishText.casefold(), polishText.casefold()}


def startsWithApplicationText(text, englishPrefix):
	"""Match a caption prefix before or after accessible-name translation."""
	value = str(text or "").replace("&", "").strip().casefold()
	polishPrefix = _APPLICATION_EN_TO_PL.get(englishPrefix, "")
	return value.startswith(englishPrefix.casefold()) or bool(polishPrefix and value.startswith(polishPrefix.casefold()))
