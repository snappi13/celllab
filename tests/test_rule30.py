from pathlib import Path
from cellab.model import Automaton


def test_load_rule30_automaton():
    automaton = Automaton.load(Path("automata") / "rule30.json")
    assert automaton.name == "Rule 30"
    assert automaton.dimensions == 1
    assert automaton.special["rule"] == 30
