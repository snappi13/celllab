from pathlib import Path

import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from .engine import run
from .model import Automaton, WorldState

ROOT = Path(__file__).resolve().parent.parent
AUTOMATA_DIR = ROOT / "automata"
WEB_DIR = ROOT / "web"

app = FastAPI(title="CelLab API")


class SimulateRequest(BaseModel):
    automaton: str
    generations: int = Field(50, ge=1, le=300)
    width: int = Field(40, ge=5, le=150)
    height: int = Field(40, ge=5, le=150)
    seed: int | None = None


def initial_world(automaton: Automaton, req: SimulateRequest) -> WorldState:
    if automaton.dimensions == 1:
        grid = np.full(req.width, automaton.default_index, dtype=np.int32)
        grid[req.width // 2] = 1
    else:
        rng = np.random.default_rng(req.seed)
        grid = rng.integers(0, len(automaton.states), size=(req.height, req.width), dtype=np.int32)
    return WorldState(generation=0, grid=grid)


@app.get("/")
def index():
    return FileResponse(WEB_DIR / "index.html")


@app.get("/automata")
def list_automata():
    return sorted(p.name for p in AUTOMATA_DIR.glob("*.json"))


@app.post("/simulate")
def simulate(req: SimulateRequest):
    path = (AUTOMATA_DIR / req.automaton).resolve()
    if path.parent != AUTOMATA_DIR.resolve() or not path.exists():
        raise HTTPException(status_code=404, detail=f"Automat inexistent: {req.automaton}")
    try:
        automaton = Automaton.load(path)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    history = run(initial_world(automaton, req), automaton, req.generations)
    return {
        "name": automaton.name,
        "dimensions": automaton.dimensions,
        "states": automaton.states,
        "generations": [w.grid.tolist() for w in history],
    }
