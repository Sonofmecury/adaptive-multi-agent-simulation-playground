from __future__ import annotations

from pathlib import Path

from simulation import MetricsTracker, MultiAgentEnvironment
from simulation.logger import SimulationLogger


def test_metrics_logger_writes_jsonl(tmp_path: Path) -> None:
    environment = MultiAgentEnvironment(seed=3)
    tracker = MetricsTracker()
    logger = SimulationLogger(tmp_path / "log.jsonl")

    metrics = tracker.record_episode(
        episode=1,
        environment=environment,
        step_resources=2,
        step_hazards=1,
        event=None,
    )
    logger.episode(metrics)

    content = (tmp_path / "log.jsonl").read_text(encoding="utf-8")

    assert '"type": "episode"' in content
    assert metrics.episode_score > 0


def test_simulation_outputs_generate_files() -> None:
    from examples.run_simulation import LOG_PATH, PLOT_PATH, run_simulation

    run_simulation(episodes=3, steps_per_episode=4, verbose=False)

    assert PLOT_PATH.exists()
    assert LOG_PATH.exists()
