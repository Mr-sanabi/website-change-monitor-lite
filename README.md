# Website Change Monitor Lite

A Python CLI tool that checks public web pages for content changes and exports a structured CSV report.

The tool reads a list of URLs, fetches each page, extracts visible text, generates a SHA256 hash, compares it with the previous saved hash, and reports whether each page is new, unchanged, or changed.

## Features

* Reads URLs from a `.txt` file
* Fetches public web pages with `requests`
* Extracts visible page text with BeautifulSoup
* Removes `script`, `style`, and `noscript` content before hashing
* Normalizes page text before comparison
* Generates SHA256 hashes for page content
* Saves previous page hashes in a JSON state file
* Detects new, unchanged, and changed pages
* Exports a CSV report
* Handles request errors without crashing
* Supports a custom state file with `--state-file`

## Why This Project

Many clients need a simple way to monitor public web pages for updates, such as:

* product availability changes
* pricing page updates
* competitor website changes
* content updates
* status or announcement page changes
* public listing page changes

This project is a lightweight first version of a website monitoring workflow.

## Tech Stack

* Python
* requests
* BeautifulSoup
* hashlib
* json
* csv
* argparse
* datetime

## Project Structure

```text
website-change-monitor-lite/
  src/
    main.py
    fetcher.py
    monitor.py
    storage.py
    logger_config.py

  data/
    .gitkeep
    urls.txt

  README.md
  requirements.txt
  .gitignore
```

## Usage

Install dependencies:

```bash
pip install -r requirements.txt
```

Add URLs to `data/urls.txt`:

```text
https://example.com
https://books.toscrape.com/
```

Run the monitor:

```bash
python src/main.py data/urls.txt data/report.csv
```

Run with a custom state file:

```bash
python src/main.py data/urls.txt data/report.csv --state-file data/custom_state.json
```

## Input

The input file should be a plain `.txt` file with one URL per line:

```text
https://example.com
https://books.toscrape.com/
https://example.org/pricing
```

Empty lines are ignored.

## Output CSV

The tool exports a CSV report with the following columns:

```text
url
status_code
changed
previous_hash
current_hash
checked_at
error
```

## Change Status Values

```text
new
```

The URL was not found in the previous state file. This usually happens on the first run.

```text
no
```

The current page hash matches the previously saved hash. No content change was detected.

```text
yes
```

The current page hash is different from the previously saved hash. A content change was detected.

## Example Output

```csv
url,status_code,changed,previous_hash,current_hash,checked_at,error
https://example.com,200,no,d003f90bc10db991b76e6fb480123cfce2cbb2b2784abe687fccccfa7ecacad8,d003f90bc10db991b76e6fb480123cfce2cbb2b2784abe687fccccfa7ecacad8,2026-06-27T11:44:36,
https://books.toscrape.com/,200,no,0b542027efb7302d70c16553548e5251d8fda055a807643342a7b80bcb0be7f9,0b542027efb7302d70c16553548e5251d8fda055a807643342a7b80bcb0be7f9,2026-06-27T11:44:36,
```

## State File

The state file stores the latest known hash for each URL:

```json
{
  "https://example.com": "d003f90bc10db991b76e6fb480123cfce2cbb2b2784abe687fccccfa7ecacad8",
  "https://books.toscrape.com/": "0b542027efb7302d70c16553548e5251d8fda055a807643342a7b80bcb0be7f9"
}
```

On each run, the tool:

1. Loads the previous state.
2. Fetches each URL.
3. Extracts and hashes visible text.
4. Compares the new hash with the previous hash.
5. Writes a CSV report.
6. Updates the state file.

## Current Limitations

This is a lightweight MVP version.

It currently:

* checks visible text content, not visual layout
* does not send email or Telegram alerts
* does not schedule automatic runs
* does not compare exact text differences
* does not handle login-protected pages
* does not bypass captchas or anti-bot systems

## Possible Improvements

Future versions could include:

* email or Telegram notifications
* scheduled monitoring
* text diff reports
* keyword-specific monitoring
* price-specific monitoring
* separate handling for request errors
* monitoring only selected page sections
* storing historical snapshots

## What I Practiced

* Building a CLI monitoring tool with `argparse`
* Reading URL lists from text files
* Fetching public pages with `requests`
* Extracting visible text with BeautifulSoup
* Cleaning and normalizing page text
* Generating SHA256 hashes
* Comparing current and previous page states
* Saving state in JSON
* Exporting CSV reports
* Structuring a Python project into clean modules

## Compliance Note

This tool is intended for monitoring publicly accessible web pages where automated access is allowed.

It does not bypass logins, captchas, paywalls, private APIs, or restricted access systems. Always respect each website’s terms of service and robots.txt.
