import yaml
from pathlib import Path

def load_yaml(path: str | Path) -> dict:
    with open(path, "r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)