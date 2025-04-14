import json
from pathlib import Path

CHANNELS_FILE = Path("app/data/channels.json")


def load_channels() -> list:
    if CHANNELS_FILE.exists():
        return json.loads(CHANNELS_FILE.read_text())
    return []


def save_channels(channels: list):
    CHANNELS_FILE.parent.mkdir(parents=True, exist_ok=True)
    CHANNELS_FILE.write_text(json.dumps(sorted(set(channels))))
