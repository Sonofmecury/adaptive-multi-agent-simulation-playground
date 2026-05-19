"""Adaptive environment controller for group performance."""

from __future__ import annotations

from dataclasses import dataclass

from simulation.environment import MultiAgentEnvironment


@dataclass(frozen=True)
class AdaptationEvent:
    """Record of a runtime environment adaptation."""

    episode: int
    action: str
    reason: str
    resource_count: int
    hazard_count: int
    safe_zone_count: int


class AdaptiveController:
    """Change environment parameters based on collective performance."""

    def __init__(self, stable_window: int = 3) -> None:
        self.stable_window = stable_window
        self.events: list[AdaptationEvent] = []
        self._stable_counter = 0

    def update(
        self,
        *,
        episode: int,
        environment: MultiAgentEnvironment,
        resources_collected: int,
        active_agents: int,
        hazard_collisions: int,
    ) -> AdaptationEvent | None:
        action = "maintain"
        reason = "performance within target band"

        if resources_collected >= 10 and hazard_collisions <= 1:
            environment.reduce_resources()
            environment.add_hazard()
            action = "increase_challenge"
            reason = f"resources_collected={resources_collected}, hazard_collisions={hazard_collisions}"
            self._stable_counter = 0
        elif (
            active_agents <= max(1, len(environment.agents) // 2)
            or hazard_collisions >= 5
        ):
            environment.increase_resources()
            environment.remove_hazard()
            action = "reduce_challenge"
            reason = (
                f"active_agents={active_agents}, hazard_collisions={hazard_collisions}"
            )
            self._stable_counter = 0
        else:
            self._stable_counter += 1
            if self._stable_counter >= self.stable_window:
                environment.introduce_safe_zone()
                environment.add_hazard()
                action = "introduce_new_challenge"
                reason = "stable group performance"
                self._stable_counter = 0

        if action == "maintain":
            return None

        event = AdaptationEvent(
            episode=episode,
            action=action,
            reason=reason,
            resource_count=environment.resource_count,
            hazard_count=environment.hazard_count,
            safe_zone_count=len(environment.safe_zones),
        )
        self.events.append(event)
        return event
