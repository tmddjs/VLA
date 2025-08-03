from typing import List, Dict, Any
from io import BytesIO

from .data import load_plants_json
from .grid import Grid
from .layout import PlantLayout
from .sunlight import default_sun_positions
from .visualize import plot_layout


def run_layout(plants: List[Dict[str, Any]], width: float, height: float, cell: float = 0.5) -> List[Dict[str, Any]]:
    plant_objs = load_plants_json(plants)
    sun_positions = default_sun_positions()
    grid = Grid(width, height, cell)
    grid.initialize_exposures(len(sun_positions))
    layout = PlantLayout(grid, sun_positions)
    layout.place_plants(plant_objs)
    buffer = BytesIO()
    plot_layout(layout, buffer)
    return layout.to_dict()
