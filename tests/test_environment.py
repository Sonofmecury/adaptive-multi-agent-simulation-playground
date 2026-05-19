from __future__ import annotations

from simulation import MultiAgentEnvironment


def test_resource_collection() -> None:
    environment = MultiAgentEnvironment(agent_policy_types=("random",), seed=1)
    agent = environment.agents[0]
    agent.position = (0, 0)
    environment.resources = {(0, 0)}
    environment.hazards = set()

    result = environment.step()

    assert result["resources_collected"] >= 1
    assert agent.collected_resources >= 1


def test_hazard_collision() -> None:
    environment = MultiAgentEnvironment(agent_policy_types=("random",), seed=1)
    agent = environment.agents[0]
    agent.position = (0, 0)
    environment.resources = set()
    environment.hazards = {(0, 0)}
    environment.safe_zones = set()

    result = environment.step()

    assert result["hazard_collisions"] >= 1
    assert agent.hazard_collisions >= 1
