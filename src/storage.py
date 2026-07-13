import json
import csv
import os
from pathlib import Path

def load_state(state_file):
    if not os.path.exists(state_file):
        return {}
    
    try:
        with open(state_file, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error loading state file: {e}")
        return {}

def save_state(state_file, state):
    path = Path(state_file)
    path.parent.mkdir(parents=True, exist_ok=True)

    temporary_path = path.with_suffix(path.suffix + ".tmp")

    with open(temporary_path, "w", encoding="utf-8") as file:
       json.dump(state, file, indent=2, ensure_ascii=False)

    temporary_path.replace(path)

def save_report(output_file, rows):
    if not rows:
        print("No report rows to save.")
        return
    
    path = Path(output_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    fields = rows[0].keys()

    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
        print(f"Saved {len(rows)} rows to {output_file}")