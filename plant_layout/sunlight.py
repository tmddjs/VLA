import math
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class SunPosition:
    elevation: float  # degrees above horizon
    azimuth: float    # degrees from north clockwise


def default_sun_positions() -> List[SunPosition]:
    # Four seasons (equinoxes and solstices) times three moments (morning, noon, afternoon)
    positions = []
    for season in range(4):
        for time in ['morning', 'noon', 'afternoon']:
            # Simple model: elevation varies with season and time of day
            base_elev = 15 + 15 * season  # 15-60 degrees
            if time == 'noon':
                elev = base_elev + 30
            elif time == 'afternoon':
                elev = base_elev + 15
            else:
                elev = base_elev
            azimuth = 90 if time == 'morning' else 180 if time == 'noon' else 270
            positions.append(SunPosition(elevation=elev, azimuth=azimuth))
    return positions


def sun_vector(pos: SunPosition) -> Tuple[float, float, float]:
    # Return unit vector components (dx, dy, dz)
    elev_rad = math.radians(pos.elevation)
    azim_rad = math.radians(pos.azimuth)
    dx = math.cos(elev_rad) * math.sin(azim_rad)
    dy = math.cos(elev_rad) * math.cos(azim_rad)
    dz = math.sin(elev_rad)
    return dx, dy, dz
