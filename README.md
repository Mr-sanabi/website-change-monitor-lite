# Website Change Monitor Lite

A Python 3.10+ CLI that compares normalized page text with its saved hash and writes a CSV report.

## Run

Create `data/urls.txt` with one public URL per line.

```bash
python -m pip install -r requirements.txt
python -m src.main data/urls.txt data/report.csv
```

State defaults to `data/state.json`; change it with `--state-file PATH`.
Results: `new`, `unchanged`, `changed`, `http_error`, or `request_error`. Failed requests preserve the previous successful hash.

## Limits

Text comparison only, not visual changes or line-by-line diffs. No scheduler, notifications, authenticated pages, or JavaScript rendering. Use only pages where automated access is permitted.

## Tests

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```
