"""Print adaptation events from a simulation run."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from examples.run_simulation import run_simulation


def main() -> None:
    tracker = run_simulation(episodes=18, steps_per_episode=20, verbose=False)
    print("episode  action                   reason")
    print("-" * 70)
    for event in tracker.adaptation_events:
        print(f"{event.episode:>7}  {event.action:<23} {event.reason}")


if __name__ == "__main__":
    main()
