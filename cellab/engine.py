from __future__ import annotations
import numpy as np
from .model import Automaton, WorldState


def _neighbor_counts_2d(grid, r, c, neighborhood, boundary, states):
    rows, cols = grid.shape
    if neighborhood == "moore":
        deltas = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    else:
        deltas = [(-1,0),(0,-1),(0,1),(1,0)]

    counts = {s: 0 for s in states}
    for dr, dc in deltas:
        nr, nc = r + dr, c + dc
        if boundary == "wrap":
            nr, nc = nr % rows, nc % cols
            counts[states[grid[nr, nc]]] += 1
        else:
            if 0 <= nr < rows and 0 <= nc < cols:
                counts[states[grid[nr, nc]]] += 1
    return counts


def _neighbor_counts_1d(grid, i, boundary, states):
    n = len(grid)
    counts = {s: 0 for s in states}
    for di in (-1, 1):
        ni = i + di
        if boundary == "wrap":
            ni = ni % n
            counts[states[grid[ni]]] += 1
        else:
            if 0 <= ni < n:
                counts[states[grid[ni]]] += 1
    return counts


def _step_elementary(world, automaton):
    rule_num = automaton.special["rule"]
    rule_bits = [(rule_num >> i) & 1 for i in range(8)]
    grid = world.grid
    n = len(grid)
    new_grid = np.zeros(n, dtype=np.int32)
    for i in range(n):
        left   = int(grid[(i - 1) % n])
        center = int(grid[i])
        right  = int(grid[(i + 1) % n])
        pattern = (left << 2) | (center << 1) | right
        new_grid[i] = rule_bits[pattern]
    return WorldState(generation=world.generation + 1, grid=new_grid)


def step(world: WorldState, automaton: Automaton) -> WorldState:
    sp = automaton.special
    if sp and sp.get("type") == "elementary":
        return _step_elementary(world, automaton)

    s2i = automaton.state_to_index
    states = automaton.states

    if automaton.dimensions == 1:
        n = len(world.grid)
        new_grid = world.grid.copy()
        for i in range(n):
            curr = states[world.grid[i]]
            nc = _neighbor_counts_1d(world.grid, i, automaton.boundary, states)
            for rule in automaton.rules:
                if rule.from_state == curr and rule.condition_holds(nc):
                    new_grid[i] = s2i[rule.to_state]
                    break
        return WorldState(generation=world.generation + 1, grid=new_grid)

    rows, cols = world.grid.shape
    new_grid = world.grid.copy()
    for r in range(rows):
        for c in range(cols):
            curr = states[world.grid[r, c]]
            nc = _neighbor_counts_2d(world.grid, r, c,
                                      automaton.neighborhood,
                                      automaton.boundary, states)
            for rule in automaton.rules:
                if rule.from_state == curr and rule.condition_holds(nc):
                    new_grid[r, c] = s2i[rule.to_state]
                    break
    return WorldState(generation=world.generation + 1, grid=new_grid)


def run(world: WorldState, automaton: Automaton, steps: int) -> list[WorldState]:
    history = [world]
    for _ in range(steps):
        history.append(step(history[-1], automaton))
    return history