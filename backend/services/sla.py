from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel


class PrioritySLA(BaseModel):
    first_response_mins: int
    resolution_mins: int


def load_sla_config(config_path: Path) -> dict[str, PrioritySLA]:
    with config_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    return {priority: PrioritySLA(**values) for priority, values in data.items()}
