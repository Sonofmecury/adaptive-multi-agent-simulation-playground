"""Run the adaptive multi-agent simulation and save outputs."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt

from simulation import AdaptiveController, MetricsTracker, MultiAgentEnvironment
from simulation.logger import SimulationLogger

OUTPUT_DIR = Path(__file__).resolve().parents[1] / "outputs"
PLOT_PATH = OUTPUT_DIR / "simulation_metrics.png"
LOG_PATH = OUTPUT_DIR / "simulation_log.jsonl"


def run_simulation(
    episodes: int = 30, steps_per_episode: int = 20, verbose: bool = True
) -> MetricsTracker:
    environment = MultiAgentEnvironment(seed=12)
    controller = AdaptiveController()
    tracker = MetricsTracker()
    logger = SimulationLogger(LOG_PATH)

    for episode in range(1, episodes + 1):
        episode_resources = 0
        episode_hazards = 0
        for _ in range(steps_per_episode):
            result = environment.step()
            episode_resources += result["resources_collected"]
            episode_hazards += result["hazard_collisions"]

        event = controller.update(
            episode=episode,
            environment=environment,
            resources_collected=episode_resources,
            active_agents=environment.active_agent_count,
            hazard_collisions=episode_hazards,
        )
        metrics = tracker.record_episode(
            episode=episode,
            environment=environment,
            step_resources=episode_resources,
            step_hazards=episode_hazards,
            event=event,
        )
        logger.episode(metrics)
        logger.adaptation(event)

        if verbose:
            print(
                f"episode={episode:02d} resources={episode_resources:02d} "
                f"active={metrics.active_agents} energy={metrics.average_agent_energy:.1f} "
                f"hazards={episode_hazards} event={event.action if event else 'none'}"
            )
        environment.reset()

    save_plot(tracker, PLOT_PATH)
    if verbose:
        print(f"\nSaved plot to {PLOT_PATH}")
        print(f"Saved log to {LOG_PATH}")
    return tracker


def save_plot(tracker: MetricsTracker, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    episodes = [item.episode for item in tracker.episodes]
    resources = [item.total_resources_collected for item in tracker.episodes]
    energy = [item.average_agent_energy for item in tracker.episodes]
    active = [item.active_agents for item in tracker.episodes]
    hazards = [item.hazard_collisions for item in tracker.episodes]

    plt.figure(figsize=(10, 6))
    plt.plot(episodes, resources, label="Total resources collected", linewidth=2)
    plt.plot(episodes, energy, label="Average energy", linewidth=2)
    plt.plot(episodes, active, label="Active agents", linewidth=2)
    plt.plot(episodes, hazards, label="Hazard collisions", linewidth=2)
    plt.xlabel("Episode")
    plt.ylabel("Metric value")
    plt.title("Adaptive Multi-Agent Simulation Metrics")
    plt.grid(alpha=0.25)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=140)
    plt.close()


def main() -> None:
    run_simulation()


if __name__ == "__main__":
    main()
