"""Small terminal renderer for quick simulation inspection."""

from __future__ import annotations

from simulation.environment import MultiAgentEnvironment


def render_environment(environment: MultiAgentEnvironment) -> str:
    rows: list[str] = []
    agent_positions = {agent.position: str(agent.agent_id) for agent in environment.agents}

    for row in range(environment.grid_size):
        cells: list[str] = []
        for col in range(environment.grid_size):
            position = (row, col)
            if position in agent_positions:
                cells.append(agent_positions[position])
            elif position in environment.resources:
                cells.append("R")
            elif position in environment.hazards:
                cells.append("H")
            elif position in environment.safe_zones:
                cells.append("S")
            else:
                cells.append(".")
        rows.append(" ".join(cells))

    return "\n".join(rows)
