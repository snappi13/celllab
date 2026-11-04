from pathlib import Path
import pytest
from cellab.model import Automaton


def test_load_life_automaton():
    automaton = Automaton.load(Path("automata") / "life.json")
    assert automaton.name == "Game of Life"
    assert automaton.dimensions == 2
    assert automaton.states == ["DEAD", "ALIVE"]
    assert len(automaton.rules) == 2


def test_missing_keys(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text('{"name": "X"}', encoding="utf-8")
    with pytest.raises(ValueError):
        Automaton.load(bad)
