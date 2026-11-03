from __future__ import annotations
import json
from dataclasses import dataclass, field
from pathlib import Path
import numpy as np


@dataclass
class Rule:
    from_state: str
    to_state: str
    condition: dict | None = None

    def condition_holds(self, neighbor_counts: dict) -> bool:
        if self.condition is None:
            return True
        count = neighbor_counts.get(self.condition["count"], 0)
        op = self.condition["op"]
        value = self.condition["value"]
        if op == "==":     return count == value
        if op == "not in": return count not in value
        if op == "in":     return count in value
        if op == ">=":     return count >= value
        if op == "<=":     return count <= value
        raise ValueError(f"Operator necunoscut: {op}")


@dataclass
class Automaton:
    name: str
    dimensions: int
    states: list[str]
    default_state: str
    neighborhood: str = "moore"
    boundary: str = "wrap"
    rules: list[Rule] = field(default_factory=list)
    special: dict | None = None

    @property
    def state_to_index(self):
        return {name: i for i, name in enumerate(self.states)}

    @property
    def default_index(self):
        return self.state_to_index[self.default_state]

    @classmethod
    def load(cls, path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        rules = [
            Rule(r["from"], r["to"], r.get("if"))
            for r in data.get("rules", [])
        ]
        return cls(
            name=data["name"],
            dimensions=data["dimensions"],
            states=data["states"],
            default_state=data["default_state"],
            neighborhood=data.get("neighborhood", "moore"),
            boundary=data.get("boundary", "wrap"),
            rules=rules,
            special=data.get("special"),
        )


@dataclass
class WorldState:
    generation: int
    grid: np.ndarray
    agents: dict | None = None

    def copy(self):
        return WorldState(
            generation=self.generation,
            grid=self.grid.copy(),
            agents=None if self.agents is None else json.loads(json.dumps(self.agents)),
        )