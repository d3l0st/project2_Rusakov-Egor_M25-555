import json


def load_metadata(filepath="db_meta.json"):
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_metadata(data, filepath="db_meta.json"):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)