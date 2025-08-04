import random
from typing import List, Tuple

from .data import Plant, load_plants
from .grid import Grid
from .sunlight import SunPosition, default_sun_positions, sun_vector
from .shadow import shadow_cells


class PlantLayout:
    def __init__(self, grid: Grid, sun_positions: List[SunPosition]):
        self.grid = grid
        self.sun_positions = sun_positions
        # Precompute sun vectors for shadow calculations
        self.sun_vectors = [sun_vector(s) for s in sun_positions]
        self.placements: List[Tuple[Plant, float, float]] = []

    def update_shadow(self, x: float, y: float, height: float):
        cells = shadow_cells(self.grid, x, y, height, self.sun_vectors)
        self.grid.mark_shadow(cells)

    def can_place(self, plant: Plant, row: int, col: int) -> bool:
        if self.grid.occupied[row, col]:
            return False
        if self.grid.exposures[row, col] < plant.light_requirement:
            return False
        return True

    def place_plants(self, plants: List[Plant]):
        random.shuffle(plants)
        for plant in plants:
            for _ in range(100):  # try 100 random cells
                row = random.randrange(self.grid.rows)
                col = random.randrange(self.grid.cols)
                if not self.can_place(plant, row, col):
                    continue
                x, y = self.grid.cell_center(row, col)
                self.placements.append((plant, x, y))
                self.grid.occupied[row, col] = True
                self.update_shadow(x, y, plant.max_height)
                break

    def to_dict(self):
        out = []
        for plant, x, y in self.placements:
            out.append({
                'scientific_name': plant.scientific_name,
                'kr_name': plant.kr_name,
                'x': x,
                'y': y,
            })
        return out


def generate_layout(csv_path: str, width: float, height: float, cell_size: float):
    sun_positions = default_sun_positions()
    grid = Grid(width, height, cell_size)
    grid.initialize_exposures(len(sun_positions))
    plants = load_plants(csv_path)
    layout = PlantLayout(grid, sun_positions)
    layout.place_plants(plants)
    return layout
