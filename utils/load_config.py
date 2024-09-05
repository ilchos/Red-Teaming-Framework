from pathlib import Path
import json

CONFIG_PATH = Path(__file__).parents[1] / "config"

def load_api_keys(fname: str = "api_keys.json"):
    keys_path = CONFIG_PATH /  fname
    api_keys = json.loads(keys_path.read_text())
    return api_keys
