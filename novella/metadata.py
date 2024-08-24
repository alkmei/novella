import os
import json


def load_metadata(metadata_path):
    if os.path.exists(metadata_path):
        with open(metadata_path, "r") as file:
            return json.load(file)
    else:
        raise FileNotFoundError(f"Story file not found: {metadata_path}")


def save_metadata(metadata, metadata_path):
    with open(metadata_path, "w") as file:
        json.dump(metadata, file, indent=4)
