"""Grid-world environment for multiple adaptive-simulation agents."""

from __future__ import annotations

import random

from simulation.agent import Agent, AgentStatus, Position
from simulation.policies import choose_action


class MultiAgentEnvironment:
    """Resource collection environment with hazards and simple safe zones."""

    def __init__(
        self,
        *,
        grid_size: int = 10,
        agent_policy_types: tuple[str, ...] = (
            "random",
            "greedy",
            "hazard_avoider",
            "energy_saver",
        ),
        seed: int | None = None,
    ) -> None:
        self.grid_size = grid_size
        self.agent_policy_types = agent_policy_types
        self.rng = random.Random(seed)
        self.resource_count = 12
        self.hazard_count = 5
        self.safe_zones: set[Position] = {(0, 0)}
        self.agents: list[Agent] = []
        self.resources: set[Position] = set()
        self.hazards: set[Position] = set()
        self.step_index = 0
        self.reset()

    def reset(self) -> None:
        self.step_index = 0
        self.agents = [
            Agent(agent_id=index, position=(0, index), policy_type=policy_type)
            for index, policy_type in enumerate(self.agent_policy_types)
        ]
        occupied = {agent.position for agent in self.agents} | self.safe_zones
        self.resources = self._sample_positions(self.resource_count, occupied)
        occupied |= self.resources
        self.hazards = self._sample_positions(self.hazard_count, occupied)

    def step(self) -> dict[str, int]:
        self.step_index += 1
        resources_collected = 0
        hazard_collisions = 0

        for agent in self.agents:
            if agent.status is not AgentStatus.ACTIVE:
                continue

            collected, collided = self._resolve_cell_interaction(agent)
            resources_collected += collected
            hazard_collisions += collided

            action = choose_action(
                agent=agent,
                resources=self.resources,
                hazards=self.hazards,
                grid_size=self.grid_size,
                rng=self.rng,
            )
            agent.move(action, self.grid_size)

            collected, collided = self._resolve_cell_interaction(agent)
            resources_collected += collected
            hazard_collisions += collided

        self._respawn_resources()
        return {
            "resources_collected": resources_collected,
            "hazard_collisions": hazard_collisions,
            "active_agents": self.active_agent_count,
        }

    @property
    def active_agent_count(self) -> int:
        return sum(agent.status is AgentStatus.ACTIVE for agent in self.agents)

    @property
    def average_energy(self) -> float:
        return sum(agent.energy for agent in self.agents) / len(self.agents)

    @property
    def total_resources_collected(self) -> int:
        return sum(agent.collected_resources for agent in self.agents)

    @property
    def total_hazard_collisions(self) -> int:
        return sum(agent.hazard_collisions for agent in self.agents)

    def reduce_resources(self, amount: int = 2) -> None:
        self.resource_count = max(4, self.resource_count - amount)
        self._trim_set(self.resources, self.resource_count)

    def increase_resources(self, amount: int = 2) -> None:
        self.resource_count = min(24, self.resource_count + amount)
        self._respawn_resources()

    def add_hazard(self) -> None:
        self.hazard_count = min(18, self.hazard_count + 1)
        occupied = (
            self.resources | self.hazards | {agent.position for agent in self.agents}
        )
        self.hazards |= self._sample_positions(1, occupied)

    def remove_hazard(self) -> None:
        self.hazard_count = max(1, self.hazard_count - 1)
        self._trim_set(self.hazards, self.hazard_count)

    def introduce_safe_zone(self) -> None:
        candidates = self._sample_positions(1, self.resources | self.hazards)
        self.safe_zones |= candidates

    def _resolve_cell_interaction(self, agent: Agent) -> tuple[int, int]:
        resources_collected = 0
        hazard_collisions = 0

        if agent.position in self.resources:
            self.resources.remove(agent.position)
            agent.collect_resource()
            resources_collected = 1

        if agent.position in self.hazards and agent.position not in self.safe_zones:
            agent.hit_hazard()
            hazard_collisions = 1

        return resources_collected, hazard_collisions

    def _respawn_resources(self) -> None:
        occupied = (
            self.resources
            | self.hazards
            | self.safe_zones
            | {agent.position for agent in self.agents}
        )
        missing = self.resource_count - len(self.resources)
        if missing > 0:
            self.resources |= self._sample_positions(missing, occupied)

    def _sample_positions(self, count: int, blocked: set[Position]) -> set[Position]:
        available = [
            (row, col)
            for row in range(self.grid_size)
            for col in range(self.grid_size)
            if (row, col) not in blocked
        ]
        if count <= 0:
            return set()
        if count > len(available):
            raise ValueError("Not enough free cells available")
        return set(self.rng.sample(available, count))

    @staticmethod
    def _trim_set(items: set[Position], target_size: int) -> None:
        while len(items) > target_size:
            items.pop()
