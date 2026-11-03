import json
from pathlib import Path
from typing import Dict, Any

class Automaton:
    def __init__(self, name: str, grid_type: str, states: int, rules: Dict[str, Any]):
        self.name = name
        self.grid_type = grid_type
        self.states = states
        self.rules = rules

    @classmethod
    def load(cls, filepath: str | Path) -> 'Automaton':
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Fișierul nu a fost găsit: {path}")

        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        required_keys = {"name", "type", "states", "rules"}
        if not required_keys.issubset(data.keys()):
            missing = required_keys - data.keys()
            raise ValueError(f"JSON invalid. Lipsesc cheile: {missing}")

        return cls(
            name=data["name"],
            grid_type=data["type"],
            states=data["states"],
            rules=data["rules"]
        )
