"""Metrics collection for adaptive multi-agent simulations."""

from __future__ import annotations

from dataclasses import dataclass

from simulation.adaptive_controller import AdaptationEvent
from simulation.environment import MultiAgentEnvironment


@dataclass(frozen=True)
class EpisodeMetrics:
    """Summary metrics for one simulation episode."""

    episode: int
    total_resources_collected: int
    average_agent_energy: float
    active_agents: int
    hazard_collisions: int
    adaptation_events: int
    episode_score: float


class MetricsTracker:
    """Track episode metrics and adaptation events."""

    def __init__(self) -> None:
        self.episodes: list[EpisodeMetrics] = []
        self.adaptation_events: list[AdaptationEvent] = []

    def record_episode(
        self,
        *,
        episode: int,
        environment: MultiAgentEnvironment,
        step_resources: int,
        step_hazards: int,
        event: AdaptationEvent | None,
    ) -> EpisodeMetrics:
        if event is not None:
            self.adaptation_events.append(event)

        score = (
            step_resources * 2.0 + environment.active_agent_count - step_hazards * 1.5
        )
        metrics = EpisodeMetrics(
            episode=episode,
            total_resources_collected=environment.total_resources_collected,
            average_agent_energy=environment.average_energy,
            active_agents=environment.active_agent_count,
            hazard_collisions=environment.total_hazard_collisions,
            adaptation_events=len(self.adaptation_events),
            episode_score=score,
        )
        self.episodes.append(metrics)
        return metrics
