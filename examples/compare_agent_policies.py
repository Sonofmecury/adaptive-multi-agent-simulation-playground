"""Compare simple policy types in the same environment."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from simulation import MultiAgentEnvironment


def evaluate_policy(policy_type: str, steps: int = 40) -> tuple[int, int, float]:
    environment = MultiAgentEnvironment(agent_policy_types=(policy_type,) * 4, seed=8)
    resources = 0
    hazards = 0
    for _ in range(steps):
        result = environment.step()
        resources += result["resources_collected"]
        hazards += result["hazard_collisions"]
    return resources, hazards, environment.average_energy


def main() -> None:
    print("policy          resources  hazards  avg_energy")
    print("-" * 48)
    for policy in ["random", "greedy", "hazard_avoider", "energy_saver"]:
        resources, hazards, average_energy = evaluate_policy(policy)
        print(f"{policy:<15} {resources:>9} {hazards:>8} {average_energy:>11.1f}")


if __name__ == "__main__":
    main()
