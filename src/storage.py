import json
import csv
import os

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
    with open(state_file, "w", encoding="utf-8") as file:
       json.dump(state, file, indent=2, ensure_ascii=False)

def save_report(output_file, rows):
    if not rows:
        print("No report rows to save.")
        return
    
    fields = rows[0].keys()

    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
        print(f"Saved {len(rows)} rows to {output_file}")