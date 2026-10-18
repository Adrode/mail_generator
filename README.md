# Mail Generator - EN

Mail Generator is a Windows desktop workflow that reads the HTML of the active Firefox tab, extracts and formats data, creates PDF documents, and opens a pre-filled message in Microsoft Outlook.

## How it works

1. Click the Mail Generator toolbar button in Firefox.
2. The extension's content script returns the current page's HTML to its background script.
3. The background script sends the HTML to the `mail_generator` native host over Firefox Native Messaging.
4. `native_host.py` reads the Native Messaging request, passes the HTML to the Outlook workflow, and returns a success or error response to the extension.
5. `html_scraper/html_scraper.py` parses the page with BeautifulSoup. It extracts the values used to build the email and populate the PDF forms.
6. `pdf_generator/create_pdf.py` overlays the extracted values onto the PDF form templates in `pdf_generator/pdf_forms/`.
7. `outlook_generator/create_outlook_template.py` creates an Outlook email, sets its subject and HTML body, attaches the generated PDFs, and displays the message for review. The message is displayed, not sent automatically.

The extension reports failures using Firefox notifications. Native-host exceptions and tracebacks are appended to `error_log.log` in the project root.

## Requirements

- Windows
- Mozilla Firefox
- Python installed and available as `python` in PowerShell
- Microsoft Outlook (Classic) desktop installed and configured on the machine
- The standard Windows Times New Roman font files (`C:\Windows\Fonts\times.ttf` and `C:\Windows\Fonts\timesbd.ttf`), used by the PDF generator

## Setup

### 1. Place the project in its configured location

For the least configuration, place the project at:

```text
C:\dev\mail_generator
```

The native-host launcher, native-host manifest, and registry file currently contain absolute paths based on this location. If you use another folder, update the paths in all three files before registering the host:

- `native_messaging_host/native_host.bat` — Python executable and `native_host.py` paths
- `native_messaging_host/native_host.json` — path to `native_host.bat`
- `native_messaging_host/register_native_host.reg` — path to `native_host.json`

The launcher expects the virtual environment to be named `env` in the project root. If you choose another environment name or location, update the Python executable path in `native_host.bat` accordingly.

### 2. Install the Firefox extension

Drag the `.xpi` package in the project root (currently `b26f959e2b164b86a7ba-1.1.xpi`) into a Firefox window and confirm installation when prompted. The extension should then appear in Firefox's toolbar or extensions menu.

### 3. Optionally limit the pages where the extension runs

By default, `get_html_extension/manifest.json` sets `content_scripts.matches` to `["<all_urls>"]`. To restrict the content script to particular pages, replace `<all_urls>` with the required Firefox match patterns, for example:

```json
"matches": ["https://example.com/*"]
```

Use the URL patterns for the pages from which the extension should read HTML. Reinstall or reload the extension after changing its manifest.

### 4. Create and activate a virtual environment

Open PowerShell in the project root and create the environment:

```powershell
python -m venv env
```

Activate it:

```powershell
.\env\Scripts\Activate.ps1
```

When activation succeeds, the environment name (for example, `(env)`) appears at the start of the PowerShell prompt. If PowerShell blocks the activation script, use an appropriately permitted execution policy for your machine, or activate the environment from a Command Prompt with `env\Scripts\activate.bat`.

### 5. Install the dependencies

With the environment active, install the packages pinned in `requirements.txt`:

```powershell
python -m pip install -r requirements.txt
```

### 6. Register the Native Messaging host

After setting up the project paths and Python environment, double-click `native_messaging_host/register_native_host.reg` and accept the Windows prompts to add the registry entry. This registers the host for the current Windows user. The registry entry points Firefox to `native_host.json`, which in turn points to the batch launcher that starts `native_host.py`.

If the project is not in `C:\dev\mail_generator`, update the hard-coded paths in the three native-host files listed above before importing the `.reg` file.

### 7. Check the PDF output directory

The PDF generator writes completed documents to `temporary_filled_forms` in the project root. Ensure this directory exists and is writable. The generated PDFs are attached to the Outlook message and then removed by the Outlook workflow.

## Project layout

```text
get_html_extension/       Firefox extension manifest and scripts
html_scraper/             HTML parsing and email/PDF data preparation
native_messaging_host/    Native-host manifest, launcher, and registry file
outlook_generator/        Outlook message composition and attachment handling
pdf_generator/            PDF generation code and source form templates
temporary_filled_forms/   Generated PDFs, temporarily stored for attachment
native_host.py            Native Messaging protocol entry point
requirements.txt          Python dependency pins
```

## Troubleshooting

- **Firefox cannot connect to the native application:** Check that the registry entry points to the correct `native_host.json`, and that the paths in the JSON and batch launcher match the project location and virtual environment.
- **The extension cannot read the active page:** Confirm the page URL matches `content_scripts.matches`, then reload the extension and page. Some browser-internal pages do not allow content scripts.
- **The email or PDFs are not generated:** Check `error_log.log` in the project root. Confirm that the page contains the HTML structure expected by the scraper, that the PDF templates are present, and that `temporary_filled_forms` is writable.
- **Outlook or PDF generation fails:** Confirm Outlook desktop is installed and available, and that the required Windows font files are present.

## Documentation

- [MDN Native messaging](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Native_messaging)
- [Beautiful Soup documentation](https://beautiful-soup-4.readthedocs.io/en/latest/)
- [pypdf documentation](https://pypdf.readthedocs.io/en/stable/)
- [ReportLab documentation](https://docs.reportlab.com/demos/hello_world/hello_world/)
- [MDN WebExtension](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Your_first_WebExtension)
- [MDN Content Scripts](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Content_scripts)
- [MDN Background Scripts](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Background_scripts)

---

# Mail Generator — PL

Mail Generator to proces działający w systemie Windows, który odczytuje kod HTML aktywnej karty Firefoksa, wyodrębnia i formatuje dane, tworzy dokumenty PDF oraz otwiera wstępnie wypełnioną wiadomość w Microsoft Outlook.

## Jak to działa

1. Kliknij przycisk Mail Generator na pasku narzędzi Firefoksa.
2. Skrypt zawartości rozszerzenia zwraca kod HTML bieżącej strony do skryptu działającego w tle.
3. Skrypt działający w tle wysyła HTML do hosta natywnego `mail_generator` za pośrednictwem Firefox Native Messaging.
4. `native_host.py` odczytuje żądanie Native Messaging, przekazuje HTML do procesu generującego wiadomość Outlook i zwraca rozszerzeniu odpowiedź o powodzeniu lub błędzie.
5. `html_scraper/html_scraper.py` przetwarza stronę za pomocą BeautifulSoup. Wyodrębnia wartości wykorzystywane do przygotowania wiadomości e-mail i wypełnienia formularzy PDF.
6. `pdf_generator/create_pdf.py` nakłada wyodrębnione wartości na szablony formularzy PDF z katalogu `pdf_generator/pdf_forms/`.
7. `outlook_generator/create_outlook_template.py` tworzy wiadomość Outlook, ustawia jej temat i treść HTML, dołącza wygenerowane pliki PDF i wyświetla wiadomość do sprawdzenia. Wiadomość jest wyświetlana, ale nie jest automatycznie wysyłana.

Rozszerzenie informuje o błędach za pomocą powiadomień Firefoksa. Wyjątki i traceback'i z hosta natywnego są dopisywane do pliku `error_log.log` w katalogu głównym projektu.

## Wymagania

- Windows
- Mozilla Firefox
- Python dostępny w PowerShellu pod poleceniem `python`
- Zainstalowana i skonfigurowana aplikacja Microsoft Outlook (Classic) na komputerze
- Standardowe pliki czcionki Times New Roman w systemie Windows (`C:\Windows\Fonts\times.ttf` i `C:\Windows\Fonts\timesbd.ttf`), używane przez generator PDF

## Konfiguracja

### 1. Umieść projekt w skonfigurowanej lokalizacji

Aby ograniczyć konieczne zmiany konfiguracji, umieść projekt w lokalizacji:

```text
C:\dev\mail_generator
```

Skrypt uruchamiający native-host, manifest native-host i plik rejestru zawierają obecnie ścieżki bezwzględne oparte na tej lokalizacji. Jeśli używasz innego katalogu, przed zarejestrowaniem hosta zaktualizuj ścieżki we wszystkich trzech plikach:

- `native_messaging_host/native_host.bat` — ścieżki do pliku Pythona i `native_host.py`
- `native_messaging_host/native_host.json` — ścieżka do `native_host.bat`
- `native_messaging_host/register_native_host.reg` — ścieżka do `native_host.json`

Skrypt uruchamiający zakłada, że środowisko wirtualne w katalogu głównym projektu nazywa się `env`. Jeśli wybierzesz inną nazwę lub lokalizację środowiska, odpowiednio zmień ścieżkę do interpretera Pythona w `native_host.bat`.

### 2. Zainstaluj rozszerzenie Firefoksa

Przeciągnij pakiet `.xpi` z katalogu głównego projektu (obecnie `b26f959e2b164b86a7ba-1.1.xpi`) do okna Firefoksa i potwierdź instalację, gdy pojawi się monit. Rozszerzenie powinno pojawić się na pasku narzędzi Firefoksa lub w menu rozszerzeń.

### 3. Opcjonalnie ogranicz strony, na których działa rozszerzenie

Domyślnie `get_html_extension/manifest.json` ustawia `content_scripts.matches` na `["<all_urls>"]`. Aby ograniczyć działanie skryptu zawartości do konkretnych stron, zastąp `<all_urls>` odpowiednimi wzorcami adresów URL obsługiwanymi przez Firefoksa, na przykład:

```json
"matches": ["https://example.com/*"]
```

Użyj wzorców adresów stron, z których rozszerzenie ma pobierać kod HTML. Po zmianie manifestu zainstaluj ponownie lub przeładuj rozszerzenie.

### 4. Utwórz i aktywuj środowisko wirtualne

Otwórz PowerShell w katalogu głównym projektu i utwórz środowisko:

```powershell
python -m venv env
```

Aktywuj je:

```powershell
.\env\Scripts\Activate.ps1
```

Po poprawnej aktywacji nazwa środowiska (na przykład `(env)`) pojawi się na początku wiersza polecenia PowerShell. Jeśli PowerShell blokuje skrypt aktywacyjny, użyj odpowiedniej dla danego komputera polityki wykonywania skryptów albo aktywuj środowisko w wierszu polecenia za pomocą `env\Scripts\activate.bat`.

### 5. Zainstaluj wymagane pakiety

Przy aktywnym środowisku zainstaluj pakiety wskazane w pliku `requirements.txt`:

```powershell
python -m pip install -r requirements.txt
```

### 6. Zarejestruj hosta Native Messaging

Po skonfigurowaniu ścieżek projektu i środowiska Pythona kliknij dwukrotnie `native_messaging_host/register_native_host.reg` i zaakceptuj monity Windows, aby dodać wpis do rejestru. Rejestruje to hosta dla bieżącego użytkownika Windows. Wpis w rejestrze wskazuje Firefoksowi plik `native_host.json`, który z kolei wskazuje skrypt uruchamiający hosta `native_host.py`.

Jeśli projekt nie znajduje się w `C:\dev\mail_generator`, przed zaimportowaniem pliku `.reg` zaktualizuj bezwzględne ścieżki w trzech wymienionych wyżej plikach native-host.

### 7. Sprawdź katalog wyjściowy plików PDF

Generator PDF zapisuje gotowe dokumenty w katalogu `temporary_filled_forms` w katalogu głównym projektu. Upewnij się, że katalog istnieje i można w nim zapisywać pliki. Wygenerowane pliki PDF są dołączane do wiadomości Outlook, a następnie usuwane przez proces obsługi wiadomości.

## Struktura projektu

```text
get_html_extension/       Manifest i skrypty rozszerzenia Firefoksa
html_scraper/             Parsowanie HTML i przygotowanie danych do e-maila/PDF
native_messaging_host/    Manifest native-host, skrypt uruchamiający i plik rejestru
outlook_generator/        Tworzenie wiadomości Outlook i obsługa załączników
pdf_generator/            Kod generujący PDF i szablony formularzy
temporary_filled_forms/   Tymczasowo przechowywane wygenerowane pliki PDF
native_host.py            Punkt wejścia protokołu Native Messaging
requirements.txt          Wersje wymaganych pakietów Pythona
```

## Rozwiązywanie problemów

- **Firefox nie może połączyć się z aplikacją natywną:** Sprawdź, czy wpis rejestru wskazuje poprawny plik `native_host.json` oraz czy ścieżki w pliku JSON i skrypcie BAT odpowiadają lokalizacji projektu i środowiska wirtualnego.
- **Rozszerzenie nie może odczytać bieżącej strony:** Upewnij się, że adres strony pasuje do `content_scripts.matches`, a następnie przeładuj rozszerzenie i stronę. Niektóre strony wewnętrzne przeglądarki nie pozwalają na uruchamianie skryptów zawartości.
- **Wiadomość lub pliki PDF nie zostały wygenerowane:** Sprawdź plik `error_log.log` w katalogu głównym projektu. Upewnij się, że strona zawiera strukturę HTML oczekiwaną przez scraper, szablony PDF są dostępne, a katalog `temporary_filled_forms` umożliwia zapis.
- **Wystąpił błąd Outlook lub generowania PDF:** Upewnij się, że aplikacja Outlook jest zainstalowana i dostępna oraz że wymagane pliki czcionek Windows są obecne.

## Dokumentacja

- [MDN Native messaging](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Native_messaging)
- [Dokumentacja Beautiful Soup](https://beautiful-soup-4.readthedocs.io/en/latest/)
- [Dokumentacja pypdf](https://pypdf.readthedocs.io/en/stable/)
- [Dokumentacja ReportLab](https://docs.reportlab.com/demos/hello_world/hello_world/)
- [MDN WebExtension](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Your_first_WebExtension)
- [MDN Content Scripts](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Content_scripts)
- [MDN Background Scripts](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Background_scripts)
