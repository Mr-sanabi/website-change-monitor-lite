# Website Change Monitor Lite

A lightweight Python CLI that monitors public web pages for visible-text changes and exports a CSV report.

The monitor fetches each URL, removes non-visible content, normalizes the remaining text, generates a SHA-256 hash, and compares it with the last successful observation. HTTP and network failures are reported without overwriting previously saved hashes.

## Features

- Reads one URL per line from a plain-text input file
- Fetches public pages with a 10-second timeout and explicit HTTP status validation
- Extracts visible text with Beautiful Soup
- Removes `script`, `style`, and `noscript` content before comparison
- Collapses repeated whitespace to reduce formatting-only changes
- Detects new, unchanged, and changed content
- Distinguishes HTTP failures from connection and request failures
- Preserves the last good hash when a fetch fails
- Saves state atomically through a temporary file
- Creates missing output directories automatically
- Exports a structured CSV report
- Includes a focused pytest regression suite

## How It Works

1. Load URLs from the input file.
2. Load the most recent successful hash for each URL.
3. Fetch every page and validate its HTTP response.
4. Extract and normalize visible text.
5. Hash the normalized text with SHA-256.
6. Compare the new hash with the saved hash.
7. Update state only after a successful fetch.
8. Write the run results to CSV.

## Project Structure

```text
website-change-monitor-lite/
├── src/
│   ├── fetcher.py
│   ├── main.py
│   ├── monitor.py
│   └── storage.py
├── tests/
│   ├── test_fetcher.py
│   ├── test_main.py
│   ├── test_monitor.py
│   └── test_storage.py
├── data/
│   └── .gitkeep
├── .gitignore
├── README.md
├── requirements.txt
└── requirements-dev.txt
```

## Requirements

- Python 3.10 or newer
- Internet access to the public pages being monitored

## Installation

```bash
git clone https://github.com/Mr-sanabi/website-change-monitor-lite.git
cd website-change-monitor-lite
python -m venv .venv
```

Activate the virtual environment.

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
source .venv/bin/activate
```

Install runtime dependencies:

```bash
python -m pip install -r requirements.txt
```

## Usage

Create a text file with one URL per line:

```text
https://example.com
https://books.toscrape.com/
```

Run the monitor from the repository root:

```bash
python -m src.main data/urls.txt data/report.csv
```

Use a custom state path:

```bash
python -m src.main data/urls.txt data/report.csv --state-file data/custom_state.json
```

Empty input lines are ignored. Missing output directories are created automatically.

## CLI Arguments

| Argument | Required | Description |
|---|---:|---|
| `input_file` | Yes | Text file containing one URL per line |
| `output_file` | Yes | Destination path for the CSV report |
| `--state-file` | No | JSON state path; defaults to `data/state.json` |

## CSV Report

The report contains these columns:

| Column | Description |
|---|---|
| `url` | URL that was checked |
| `status_code` | HTTP status when available |
| `changed` | Monitoring result or failure type |
| `previous_hash` | Last successfully saved hash |
| `current_hash` | Hash produced by the current successful fetch |
| `checked_at` | Local ISO 8601 check timestamp, precise to seconds |
| `error` | Error details for failed requests |

### Result Values

| Value | Meaning | State updated? |
|---|---|---:|
| `new` | First successful observation of the URL | Yes |
| `unchanged` | Current hash matches the saved hash | Yes |
| `changed` | Current hash differs from the saved hash | Yes |
| `http_error` | The server returned an HTTP error such as 404 or 500 | No |
| `request_error` | The request failed before a valid HTTP response was available | No |

Example:

```csv
url,status_code,changed,previous_hash,current_hash,checked_at,error
https://example.com,200,unchanged,d003f90b...,d003f90b...,2026-07-13T13:06:26,
https://example.com/missing,404,http_error,,,2026-07-13T13:06:27,404 Client Error
```

## State Safety

The JSON state file stores only the latest successful hash for each URL:

```json
{
  "https://example.com": "d003f90bc10db991b76e6fb480123cfce2cbb2b2784abe687fccccfa7ecacad8"
}
```

Failed fetches never replace a previously saved hash. State is written to a temporary sibling file and replaces the main JSON file only after serialization completes successfully.

## Tests

Install development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Run the complete test suite:

```bash
python -m pytest -v
```

The regression suite covers visible-text extraction, SHA-256 stability, atomic state storage, HTTP error classification, and preservation of the last good hash after a request failure.

## Limitations

- Monitors normalized visible text, not visual layout
- Does not produce a line-by-line text diff
- Does not schedule runs or send notifications
- Does not support authenticated pages
- Does not bypass captchas, paywalls, or anti-bot protections
- Dynamic client-rendered content may require a browser-based implementation

## Compliance

This project is intended for public pages where automated access is permitted. Respect each site's terms of service, robots.txt rules, rate limits, and applicable laws.
