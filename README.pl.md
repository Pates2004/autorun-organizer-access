# Autorun Organizer Access

Dodatek NVDA poprawiający obsługę klawiaturą klasycznego interfejsu Autorun Organizer 6.x.

Dodatek został przygotowany i sprawdzony z Autorun Organizer 6.32 oraz NVDA 2026.1.1. Wersja Autorun Organizer 7.0 używa innej listy renderowanej przez Sciter i nie jest obsługiwana w tym wydaniu.

## Możliwości

- Nadaje nazwy liście elementów autostartu i polu wyszukiwania.
- Zamienia nienazwane panele Scitera w obsługiwane klawiaturą filtry, zakładki i przełączniki.
- Dodaje bezpośrednie polecenia do najważniejszych części programu.
- Udostępnia wszystkie polecenia w oknie Zdarzenia wejścia NVDA.
- Zawiera komunikaty angielskie i pełne tłumaczenie polskie.

## Instalacja

Pobierz plik `.nvda-addon` z najnowszego wydania GitHub, otwórz go przy uruchomionym NVDA, potwierdź instalację i uruchom NVDA ponownie.

## Skróty

| Skrót | Działanie |
| --- | --- |
| NVDA+Alt+L | Przejście do listy elementów autostartu |
| NVDA+Alt+F | Przejście do wyszukiwarki |
| NVDA+Alt+1 | Widok Najważniejsze |
| NVDA+Alt+2 | Widok Wszystkie |
| NVDA+Alt+3 | Widok Niestandardowe |
| NVDA+Alt+S | Przełączenie wybranego elementu |
| NVDA+Alt+N | Przełączenie powiadomień programu |
| NVDA+Alt+A | Zakładka Aplikacja |
| NVDA+Alt+B | Zakładka Czas uruchamiania |
| NVDA+Alt+D | Odczyt dostępnych szczegółów |
| NVDA+Alt+H | Przypomnienie poleceń dodatku |

Każdy skrót można zmienić albo usunąć w **menu NVDA → Ustawienia → Zdarzenia wejścia → Autorun Organizer**.

Na wirtualnych filtrach i zakładkach pozycję wybiera się strzałkami, a aktywuje Enterem lub spacją. Enter i spacja obsługują również przełączniki.

## Zgodność i ograniczenia

Kontrolki Scitera w Autorun Organizer 6.x nie udostępniają wewnętrznych elementów przez UI Automation. Dodatek aktywuje je za pomocą położeń względnych wewnątrz bieżącego prostokąta kontrolki. Nie używa stałych współrzędnych ekranu, ale duża zmiana interfejsu może wymagać aktualizacji dodatku.

Projekt nie zawiera programu Autorun Organizer i nie jest powiązany z ChemTable Software.

## Budowanie i testy

Uruchom:

```powershell
.\test.ps1
```

Gotowy pakiet zostanie zapisany w katalogu `dist`.

## Licencja

Copyright © 2026 Patryk (Pates2004).

Dodatek jest udostępniany na licencji GNU General Public License w wersji 2 lub, według wyboru użytkownika, dowolnej późniejszej. Pełny tekst znajduje się w [COPYING.txt](COPYING.txt).
