"""Public API for generating plant layouts.

This module exposes a :func:`run_layout` helper used by the web API.  The
function accepts layout parameters and a list of plant descriptors, runs the
shadow-aware placement algorithm and optionally returns a base64 encoded PNG
visualisation of the resulting layout.
"""

from __future__ import annotations

from io import BytesIO
import base64
from typing import Any, Dict, List, Optional, Tuple

from .data import load_plants_json
from .grid import Grid
from .layout import PlantLayout
from .sunlight import default_sun_positions
from .visualize import plot_layout


def run_layout(
    width: float,
    height: float,
    plants_json: List[Dict[str, Any]],
    *,
    cell_size: float = 0.5,
    return_image: bool = True,
) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    """Generate a plant placement layout.

    Parameters
    ----------
    width, height:
        Dimensions of the target area in metres.
    plants_json:
        List of plant descriptors.  Keys may use either the English or Korean
        field names understood by :func:`load_plants_json`.
    cell_size:
        Size of the grid cell in metres.  Defaults to ``0.5``.
    return_image:
        When ``True`` the function also renders the layout to a PNG image and
        returns it encoded as base64.

    Returns
    -------
    placements:
        A list of placement dictionaries.
    image_b64:
        Base64 encoded PNG string when ``return_image`` is ``True`` otherwise
        ``None``.
    """

    plants = load_plants_json(plants_json)
    sun_positions = default_sun_positions()
    grid = Grid(width, height, cell_size)
    grid.initialize_exposures(len(sun_positions))

    layout = PlantLayout(grid, sun_positions)
    layout.place_plants(plants)

    image_b64: Optional[str] = None
    if return_image:
        buf = BytesIO()
        # ``plot_layout`` can accept file like objects which allows us to
        # generate the PNG entirely in memory.
        plot_layout(layout, buf)
        buf.seek(0)
        image_b64 = base64.b64encode(buf.read()).decode("ascii")

    return layout.to_dict(), image_b64


__all__ = ["run_layout"]

