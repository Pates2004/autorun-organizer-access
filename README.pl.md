# Autorun Organizer Access

Dodatek NVDA zapewniający pełną obsługę klawiaturą klasycznego interfejsu Autorun Organizer 6.x oraz niezależny wybór polskich lub angielskich komunikatów mowy i brajla.

Dodatek obsługuje całą rodzinę klasycznych wersji 6.x. Został bezpośrednio przetestowany z Autorun Organizer 6.32 i NVDA 2026.1.1. Przeprojektowany interfejs Autorun Organizer 7.x nie jest obsługiwany.

## Możliwości

- Nadaje nazwy liście autostartu, wyszukiwarce, paskowi stanu, górnym przyciskom ikonowym i działaniom na pasku stanu.
- Zamienia niedostępne filtry, zakładki i przełączniki Scitera w kontrolki obsługiwane klawiaturą przez NVDA.
- Pozwala aktywować Enterem i spacją klikalne etykiety VCL oraz przyciski wyboru typu wpisu autostartu.
- Udostępnia bezpośrednie polecenia do wszystkich obszarów klasycznego okna głównego.
- Pokazuje wszystkie 22 polecenia w Zdarzeniach wejścia NVDA. Przypisane klawisze działają tylko wtedy, gdy fokus znajduje się w Autorun Organizer 6.x.
- Tłumaczy na polski nazwy Autorun Organizer udostępnione NVDA przez UI Automation lub MSAA: główny widok, menu, typowe okna dialogowe, ustawienia, powiadomienia, dodawanie wpisu i Centrum cofania zmian.
- Pozostawia działania usuwające dane w menu i oknach potwierdzenia samego programu.

## Stan w menu kontekstowym

Po otwarciu menu kontekstowego elementu autostartu pozycje stanowe, takie jak
**Wyłącz** lub **Włącz**, są odczytywane wraz ze stanem: **zaznaczone** albo
**niezaznaczone**. Działa to zarówno dla UI Automation, jak i dla starszego
interfejsu VCL/MSAA programu. Jeżeli program nie udostępni stanu, NVDA poda
**stan zaznaczenia niedostępny** zamiast zgadywać.

## Ustawienie języka

Otwórz **Ustawienia NVDA → Autorun Organizer Access** i wybierz:

- **Zgodnie z językiem systemu Windows (domyślnie)**: polski Windows wybiera polski, a każdy inny język systemu wybiera angielski.
- **Angielski**.
- **Polski**.
- **Zgodnie z językiem Autorun Organizer**: aktywne polskie tłumaczenie programu wybiera polski; wbudowany angielski i każdy nieobsługiwany język programu wybierają angielski.

Ustawienie jest niezależne od języka interfejsu NVDA. Steruje komunikatami dodatku, opisami poleceń i tekstem programu odczytywanym przez NVDA lub pokazywanym na monitorze brajlowskim. Nie może zmieniać napisów rysowanych wizualnie wewnątrz procesu Autorun Organizer. Po zmianie ustawienia otwórz ponownie widoczne menu lub okno programu, aby NVDA utworzył jego obiekty dostępności w wybranym języku.

## Dlaczego nie ma już „pole wyboru, nieoznaczone”

Autorun Organizer rysuje przełącznik wybranego wpisu w Sciterze, ale nie podaje NVDA jego bieżącego stanu. Poprzednia rola pola wyboru powodowała fałszywy komunikat **nieoznaczone**. Od wersji 1.3.0 jest to uczciwie opisany przycisk akcji **Włącz lub wyłącz wybrany element autostartu**. Po aktywacji dodatek informuje, że polecenie wysłano, ale wynikowy stan nie jest dostępny dla NVDA.

Tak samo działają przełączniki powiadomień i pomiaru uruchamiania systemu. Faktyczną zmianę wykonuje program.

## Instalacja

Pobierz plik `.nvda-addon` z najnowszego wydania GitHub, otwórz go przy uruchomionym NVDA, potwierdź instalację i uruchom NVDA ponownie.

## Skróty

| Domyślny skrót | Działanie |
| --- | --- |
| NVDA+Alt+L | Przenieś fokus do listy elementów autostartu |
| NVDA+Alt+F | Przenieś fokus do wyszukiwarki |
| NVDA+Alt+1 | Wybierz widok Najważniejsze |
| NVDA+Alt+2 | Wybierz widok Wszystkie |
| NVDA+Alt+3 | Wybierz widok Niestandardowe |
| NVDA+Alt+4 | Otwórz menu lokalizacji autostartu |
| NVDA+Alt+S | Włącz lub wyłącz wybrany element autostartu |
| NVDA+Alt+C | Otwórz polecenia wybranego elementu |
| NVDA+Alt+N | Przełącz powiadomienia o nowych elementach |
| NVDA+Alt+Shift+N | Otwórz centrum powiadomień |
| NVDA+Alt+A | Otwórz zakładkę Aplikacja |
| NVDA+Alt+B | Otwórz zakładkę Czas uruchamiania |
| NVDA+Alt+Shift+B | Przełącz pomiar każdego uruchomienia systemu |
| NVDA+Alt+D | Odczytaj szczegóły elementu i bieżącej zakładki |
| NVDA+Alt+M | Otwórz Ustawienia i polecenia |
| NVDA+Alt+U | Otwórz Cofnij zmiany |
| NVDA+Alt+H | Podaj domyślne polecenia |
| Nieprzypisany | Otwórz recenzje |
| Nieprzypisany | Przełącz motyw interfejsu |
| Nieprzypisany | Otwórz Funkcje w tle |
| Nieprzypisany | Przenieś fokus do Uruchom ponownie i zmierz |
| Nieprzypisany | Przenieś fokus do częstotliwości wyłączania i opóźniania |

Wszystkie 22 polecenia są zawsze widoczne w **menu NVDA → Ustawienia → Zdarzenia wejścia → Autorun Organizer Access**. Każdy skrót można zmienić lub usunąć; można też przypisać skrót do polecenia oznaczonego jako nieprzypisane.

Na wirtualnym filtrze lub zakładce szczegółów użyj strzałek, aby wybrać pozycję, a Enteru albo spacji, aby ją aktywować. Enter i spacja aktywują też wirtualne przyciski akcji, klikalne etykiety, przyciski wyboru i nazwane przez dodatek ikony.

## Zgodność i ograniczenia

Sciter w Autorun Organizer 6.x nie udostępnia wewnętrznych elementów ani stanów przełączników przez UI Automation. Dodatek aktywuje je według położenia względnego w aktualnym prostokącie kontrolki, a nie według stałych współrzędnych ekranu. Klasyfikuje też stabilne panele VCL według rodzica, wymiarów i względnego położenia.

Tłumaczenie dostępności może przetworzyć wyłącznie tekst, który Autorun Organizer udostępnia NVDA. Tekst namalowany tylko w Sciterze, nietypowe dynamiczne treści z serwera i nazwy ról pochodzące z samego NVDA pozostają poza kontrolą dodatku. Widoczny interfejs programu nie jest modyfikowany.

Bezpośrednie testy regresji wykonano z wersją 6.32. Dodatek dopuszcza wszystkie wersje 6.x korzystające z klasycznego układu, ale odrzuca 7.x.

Projekt nie zawiera programu Autorun Organizer i nie jest powiązany z ChemTable Software.

## Budowanie i testy

Wymagania: Windows PowerShell 5.1 lub nowszy i Python 3.13. Uruchom:

```powershell
.\test.ps1
```

Gotowy pakiet zostanie zapisany w katalogu `dist`.

## Licencja

Copyright © 2026 Patryk (Pates2004).

Dodatek jest udostępniany na licencji GNU General Public License w wersji 2 lub, według wyboru użytkownika, dowolnej późniejszej. Pełny tekst znajduje się w [COPYING.txt](COPYING.txt).
