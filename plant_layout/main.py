import argparse
import json
from pathlib import Path

from .layout import generate_layout
from .visualize import plot_layout


def main():
    parser = argparse.ArgumentParser(description="Shadow-aware plant layout generator")
    parser.add_argument("csv", help="Path to plants.csv")
    parser.add_argument("width", type=float, help="Width of area in meters")
    parser.add_argument("height", type=float, help="Height of area in meters")
    parser.add_argument("--cell", type=float, default=0.5, help="Grid cell size in meters")
    parser.add_argument("--out", default="output", help="Output directory")
    args = parser.parse_args()

    layout = generate_layout(args.csv, args.width, args.height, args.cell)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    with open(out_dir / "placement.json", "w", encoding="utf-8") as f:
        json.dump(layout.to_dict(), f, ensure_ascii=False, indent=2)

    plot_layout(layout, str(out_dir / "layout.png"))


if __name__ == "__main__":
    main()
