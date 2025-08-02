import argparse
import json
from pathlib import Path

from .data import load_plants_json
from .layout import generate_layout, PlantLayout
from .grid import Grid
from .sunlight import default_sun_positions
from .visualize import plot_layout


def main():
    parser = argparse.ArgumentParser(description="Shadow-aware plant layout generator")
    parser.add_argument("width", type=float, help="Width of area in meters")
    parser.add_argument("height", type=float, help="Height of area in meters")
    parser.add_argument("csv", nargs="?", help="Path to plants.csv")
    parser.add_argument("--json", help="JSON string with plant data")
    parser.add_argument("--cell", type=float, default=0.5, help="Grid cell size in meters")
    parser.add_argument("--out", default="output", help="Output directory")
    args = parser.parse_args()

    if args.json:
        plant_obj = json.loads(args.json)
        plants = load_plants_json(plant_obj)
        sun_positions = default_sun_positions()
        grid = Grid(args.width, args.height, args.cell)
        grid.initialize_exposures(len(sun_positions))
        layout = PlantLayout(grid, sun_positions)
        layout.place_plants(plants)
    else:
        if not args.csv:
            parser.error("CSV path or --json must be provided")
        layout = generate_layout(args.csv, args.width, args.height, args.cell)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    with open(out_dir / "placement.json", "w", encoding="utf-8") as f:
        json.dump(layout.to_dict(), f, ensure_ascii=False, indent=2)

    plot_layout(layout, str(out_dir / "layout.png"))


if __name__ == "__main__":
    main()
