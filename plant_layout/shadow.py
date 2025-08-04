from typing import Dict, List, Tuple, Optional
import math

from .grid import Grid


# Cache for precomputed shadow paths based on plant height.
_shadow_cache: Dict[float, List[List[Tuple[int, int]]]] = {}


def compute_shadow_paths(
    grid: Grid, height: float, sun_vectors: List[Tuple[float, float, float]]
) -> List[List[Tuple[int, int]]]:
    """Return relative cell paths for each sun vector.

    Paths are cached by ``height`` so that multiple plants with the same height
    reuse the computed cell offsets.
    """

    if height in _shadow_cache:
        return _shadow_cache[height]

    step = grid.cell_size / 2
    paths: List[List[Tuple[int, int]]] = []
    for dx, dy, dz in sun_vectors:
        if dz <= 0:
            paths.append([])
            continue

        max_dist = math.hypot(grid.width, grid.height)
        length = min(height / dz, max_dist)
        dist = step
        cells: List[Tuple[int, int]] = []
        prev: Optional[Tuple[int, int]] = None
        while dist <= length:
            dr = math.floor(0.5 + (dy * dist) / grid.cell_size)
            dc = math.floor(0.5 + (dx * dist) / grid.cell_size)
            cell = (dr, dc)
            if cell != prev:
                cells.append(cell)
                prev = cell
            dist += step
        paths.append(cells)

    _shadow_cache[height] = paths
    return paths


def shadow_cells(
    grid: Grid,
    x: float,
    y: float,
    height: float,
    sun_vectors: List[Tuple[float, float, float]],
) -> List[Tuple[int, int]]:
    """Return cells shadowed by a plant at ``x, y`` with ``height``.

    Precomputed paths for the given ``height`` are reused for efficiency.
    """

    paths = compute_shadow_paths(grid, height, sun_vectors)
    base_row, base_col = grid.cell_indices(x, y)
    cells: List[Tuple[int, int]] = []
    for path in paths:
        cells.extend((base_row + r, base_col + c) for r, c in path)
    return cells
