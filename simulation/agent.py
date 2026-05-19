"""Agent state for the multi-agent simulation."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


Position = tuple[int, int]


class AgentStatus(str, Enum):
    """Lifecycle state for an agent."""

    ACTIVE = "active"
    EXHAUSTED = "exhausted"


@dataclass
class Agent:
    """A lightweight grid-world agent."""

    agent_id: int
    position: Position
    policy_type: str
    energy: int = 20
    collected_resources: int = 0
    hazard_collisions: int = 0
    status: AgentStatus = AgentStatus.ACTIVE

    def move(self, delta: Position, grid_size: int) -> None:
        if self.status is not AgentStatus.ACTIVE:
            return

        row, col = self.position
        row_delta, col_delta = delta
        self.position = (
            max(0, min(grid_size - 1, row + row_delta)),
            max(0, min(grid_size - 1, col + col_delta)),
        )
        self.energy -= 1
        if self.energy <= 0:
            self.energy = 0
            self.status = AgentStatus.EXHAUSTED

    def collect_resource(self, energy_bonus: int = 3) -> None:
        self.collected_resources += 1
        self.energy += energy_bonus

    def hit_hazard(self, penalty: int = 5) -> None:
        self.hazard_collisions += 1
        self.energy = max(0, self.energy - penalty)
        if self.energy == 0:
            self.status = AgentStatus.EXHAUSTED
