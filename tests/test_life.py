from pathlib import Path
from cellab.model import Automaton


def test_load_life_automaton():

    filepath = Path("automata") / "life.json"


    automaton = Automaton.load(filepath)

    assert automaton.name == "Game of Life"
    assert automaton.grid_type == "2D"
    assert automaton.states == 2
    assert "survive" in automaton.rules
    assert "birth" in automaton.rules
