import argparse
from src.fetcher import fetch_page
from src.monitor import extract_visible_text, generate_hash
from src.storage import load_state, save_state, save_report
from datetime import datetime


def parse_args():

    parser = argparse.ArgumentParser(
        description="Check public web pages for changes and export a CSV report."
    )
    parser.add_argument("input_file")
    parser.add_argument("output_file")
    parser.add_argument("--state-file", type=str, default="data/state.json")
    return parser.parse_args()

def load_urls(input_file):
    urls = []
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                clean_url = line.strip()

                if not clean_url:
                    continue
                    
                urls.append(clean_url)
            
            return urls
    except FileNotFoundError:
        print(f"File not found: {input_file}")
        return []

def main():
    args = parse_args()

    urls = load_urls(args.input_file)
    state = load_state(args.state_file)

    rows = []

    for url in urls:
        result = fetch_page(url)

        checked_at = datetime.now().isoformat(timespec="seconds")
        previous_hash = state.get(url)

        if result["error_type"] is not None:
            error_row = {
                "url": url,
                "status_code": result["status_code"],
                "changed": result["error_type"],
                "previous_hash": previous_hash if previous_hash else "",
                "current_hash": "",
                "checked_at": checked_at,
                "error": result["error"]
            }
            rows.append(error_row)
            continue

        text = extract_visible_text(result["html"])
        page_hash = generate_hash(text)

        if previous_hash is None:
            changed = "new"
        elif previous_hash == page_hash:
            changed = "unchanged"
        else:
            changed = "changed"

        state[url] = page_hash
        row = {
            "url": url,
            "status_code": result["status_code"],
            "changed": changed,
            "previous_hash": previous_hash if previous_hash else "",
            "current_hash": page_hash,
            "checked_at": checked_at,
            "error": result["error"]
        }
        rows.append(row)

    save_state(args.state_file, state)
    save_report(args.output_file, rows)


if __name__ == "__main__":
    main()