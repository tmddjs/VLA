from typing import List, Tuple
import math

from .grid import Grid
from .sunlight import SunPosition, sun_vector


def shadow_cells(grid: Grid, x: float, y: float, height: float, sun: SunPosition) -> List[Tuple[int, int]]:
    dx, dy, dz = sun_vector(sun)
    if dz <= 0:
        return []
    length = height / dz
    step = grid.cell_size / 2
    cells = []
    dist = step
    while dist <= length:
        px = x + dx * dist
        py = y + dy * dist
        r, c = grid.cell_indices(px, py)
        cells.append((r, c))
        dist += step
    return cells
