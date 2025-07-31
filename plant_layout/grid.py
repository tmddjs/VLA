from dataclasses import dataclass
from typing import List, Tuple
import numpy as np

@dataclass
class Grid:
    width: float
    height: float
    cell_size: float

    def __post_init__(self):
        self.cols = int(self.width / self.cell_size)
        self.rows = int(self.height / self.cell_size)
        self.exposures = None  # will be numpy array rows x cols
        self.occupied = np.zeros((self.rows, self.cols), dtype=bool)

    def initialize_exposures(self, total_sun_positions: int):
        self.exposures = np.full((self.rows, self.cols), total_sun_positions, dtype=int)

    def cell_center(self, row: int, col: int) -> Tuple[float, float]:
        x = (col + 0.5) * self.cell_size
        y = (row + 0.5) * self.cell_size
        return x, y

    def cell_indices(self, x: float, y: float) -> Tuple[int, int]:
        col = int(x / self.cell_size)
        row = int(y / self.cell_size)
        return row, col

    def mark_shadow(self, cells: List[Tuple[int, int]]):
        for r, c in cells:
            if 0 <= r < self.rows and 0 <= c < self.cols:
                self.exposures[r, c] -= 1
                if self.exposures[r, c] < 0:
                    self.exposures[r, c] = 0
