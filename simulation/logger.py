"""JSONL logging for multi-agent simulation runs."""

from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path

from simulation.adaptive_controller import AdaptationEvent
from simulation.metrics import EpisodeMetrics


class SimulationLogger:
    """Write episode metrics and adaptation events to JSONL."""

    def __init__(self, output_path: str | Path) -> None:
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path.write_text("", encoding="utf-8")

    def episode(self, metrics: EpisodeMetrics) -> None:
        self._write({"type": "episode", **asdict(metrics)})

    def adaptation(self, event: AdaptationEvent | None) -> None:
        if event is None:
            return
        self._write({"type": "adaptation", **asdict(event)})

    def _write(self, payload: dict[str, object]) -> None:
        with self.output_path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(payload) + "\n")
