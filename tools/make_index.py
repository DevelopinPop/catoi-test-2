"""Writes contests/index.json: the ids of every folder in contests/ that has a meta.json."""
import json, os

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "contests")
ids = sorted(d for d in os.listdir(root) if os.path.isfile(os.path.join(root, d, "meta.json")))
with open(os.path.join(root, "index.json"), "w") as f:
    json.dump({"contests": ids}, f, indent=1)
print("contests:", ids)
