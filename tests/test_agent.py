from __future__ import annotations

from simulation.agent import Agent, AgentStatus


def test_agent_movement_clamps_to_grid() -> None:
    agent = Agent(agent_id=1, position=(0, 0), policy_type="random")

    agent.move((-1, 0), grid_size=5)

    assert agent.position == (0, 0)
    assert agent.energy == 19


def test_agent_becomes_exhausted_when_energy_reaches_zero() -> None:
    agent = Agent(agent_id=1, position=(0, 0), policy_type="random", energy=1)

    agent.move((0, 1), grid_size=5)

    assert agent.status is AgentStatus.EXHAUSTED
