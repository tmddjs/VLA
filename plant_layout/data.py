from dataclasses import dataclass
from typing import List, Dict, Sequence
import csv

@dataclass
class Plant:
    scientific_name: str
    kr_name: str
    life_form: str
    max_height: float
    root_depth_min: float
    root_depth_max: float
    light_requirement: int
    lifespan: int


FIELD_ALIASES: Dict[str, Sequence[str]] = {
    "scientific_name": ["scientific_name", "학명"],
    "kr_name": ["kr_name", "국명"],
    "life_form": ["life_form", "생활형"],
    "max_height_m": ["max_height_m", "최대높이(m)"],
    "root_depth_cm_range": ["root_depth_cm_range", "뿌리깊이(cm·범위)"],
    "light_requirement_1_5": ["light_requirement_1_5", "필요광량(1-5)"],
    "lifespan_yr": ["lifespan_yr", "전형수명(년)"],
}


def _get(row: Dict[str, str], keys: Sequence[str], default: str = "") -> str:
    for k in keys:
        if k in row and row[k] != "":
            return row[k]
    return default


def load_plants(path: str) -> List[Plant]:
    plants: List[Plant] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            depth_raw = _get(row, FIELD_ALIASES["root_depth_cm_range"])
            depth_range = depth_raw.replace(" ", "").split("-") if depth_raw else ["0"]
            if len(depth_range) == 2:
                depth_min, depth_max = map(float, depth_range)
            else:
                depth_min = depth_max = float(depth_range[0])

            plants.append(
                Plant(
                    scientific_name=_get(row, FIELD_ALIASES["scientific_name"]),
                    kr_name=_get(row, FIELD_ALIASES["kr_name"]),
                    life_form=_get(row, FIELD_ALIASES["life_form"]),
                    max_height=float(_get(row, FIELD_ALIASES["max_height_m"], "0")),
                    root_depth_min=depth_min,
                    root_depth_max=depth_max,
                    light_requirement=int(_get(row, FIELD_ALIASES["light_requirement_1_5"], "3")),
                    lifespan=int(_get(row, FIELD_ALIASES["lifespan_yr"], "0")),
                )
            )
    return plants
