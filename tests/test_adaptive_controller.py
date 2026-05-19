from __future__ import annotations

from simulation import AdaptiveController, MultiAgentEnvironment


def test_adaptive_controller_increases_challenge_when_collection_is_easy() -> None:
    environment = MultiAgentEnvironment(seed=2)
    controller = AdaptiveController()

    event = controller.update(
        episode=1,
        environment=environment,
        resources_collected=12,
        active_agents=4,
        hazard_collisions=0,
    )

    assert event is not None
    assert event.action == "increase_challenge"
    assert environment.hazard_count == 6


def test_adaptive_controller_reduces_challenge_when_agents_fail() -> None:
    environment = MultiAgentEnvironment(seed=2)
    controller = AdaptiveController()

    event = controller.update(
        episode=1,
        environment=environment,
        resources_collected=1,
        active_agents=1,
        hazard_collisions=6,
    )

    assert event is not None
    assert event.action == "reduce_challenge"
    assert environment.resource_count > 12
