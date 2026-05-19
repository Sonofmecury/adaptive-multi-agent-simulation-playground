"""Simple policies for agents in the playground."""

from __future__ import annotations

import random

from simulation.agent import Agent, Position

ACTIONS: tuple[Position, ...] = ((-1, 0), (1, 0), (0, -1), (0, 1), (0, 0))


def choose_action(
    *,
    agent: Agent,
    resources: set[Position],
    hazards: set[Position],
    grid_size: int,
    rng: random.Random,
) -> Position:
    """Choose an action from a small set of interpretable policy types."""

    if agent.policy_type == "greedy":
        return (
            _toward_nearest(agent.position, resources)
            if resources
            else rng.choice(ACTIONS)
        )
    if agent.policy_type == "hazard_avoider":
        return _avoid_hazards(agent.position, hazards, grid_size, rng)
    if agent.policy_type == "energy_saver":
        return (
            (0, 0) if agent.energy < 6 and rng.random() < 0.5 else rng.choice(ACTIONS)
        )
    return rng.choice(ACTIONS)


def _toward_nearest(position: Position, targets: set[Position]) -> Position:
    target = min(targets, key=lambda item: _distance(position, item))
    row, col = position
    target_row, target_col = target
    if abs(target_row - row) >= abs(target_col - col):
        return (1 if target_row > row else -1 if target_row < row else 0, 0)
    return (0, 1 if target_col > col else -1 if target_col < col else 0)


def _avoid_hazards(
    position: Position,
    hazards: set[Position],
    grid_size: int,
    rng: random.Random,
) -> Position:
    candidates = list(ACTIONS)
    rng.shuffle(candidates)
    best_action = (0, 0)
    best_score = -1
    for action in candidates:
        candidate = _clip((position[0] + action[0], position[1] + action[1]), grid_size)
        nearest_hazard = min(
            (_distance(candidate, hazard) for hazard in hazards), default=grid_size
        )
        if candidate not in hazards and nearest_hazard > best_score:
            best_score = nearest_hazard
            best_action = action
    return best_action


def _clip(position: Position, grid_size: int) -> Position:
    return (
        max(0, min(grid_size - 1, position[0])),
        max(0, min(grid_size - 1, position[1])),
    )


def _distance(first: Position, second: Position) -> int:
    return abs(first[0] - second[0]) + abs(first[1] - second[1])
