from pathlib import Path
from cellab.model import Automaton


def test_load_rule30_automaton():
    filepath = Path("automata") / "rule30.json"
    automaton = Automaton.load(filepath)

    assert automaton.name == "Rule 30"
    assert automaton.grid_type == "1D"
    assert automaton.states == 2
    assert "rule_number" in automaton.rules
    assert automaton.rules["rule_number"] == 30