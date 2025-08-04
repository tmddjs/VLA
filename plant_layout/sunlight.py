import math
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class SunPosition:
    elevation: float  # degrees above horizon
    azimuth: float    # degrees from north clockwise
    weight: float = 1.0  # relative light intensity (0-1)


def sun_positions(latitude: float, samples_per_day: int = 24) -> List[SunPosition]:
    """Calculate seasonal sun positions for a given latitude.

    Args:
        latitude: Latitude in degrees (positive north).
        samples_per_day: Number of time samples per simulated day.

    Returns:
        A list of :class:`SunPosition` objects containing sun elevation and
        azimuth angles for the four principal seasons. Positions where the sun
        is below the horizon are discarded.
    """

    def _solar_position(lat_rad: float, decl: float, hour_angle: float) -> Tuple[float, float]:
        """Compute solar elevation and azimuth from latitude, declination and hour angle."""
        sin_elev = (
            math.sin(lat_rad) * math.sin(decl)
            + math.cos(lat_rad) * math.cos(decl) * math.cos(hour_angle)
        )
        elev = math.asin(sin_elev)

        sin_az = math.sin(hour_angle) * math.cos(decl) / math.cos(elev)
        cos_az = (
            math.sin(decl) - math.sin(elev) * math.sin(lat_rad)
        ) / (math.cos(elev) * math.cos(lat_rad))
        az = math.atan2(sin_az, cos_az)
        return math.degrees(elev), (math.degrees(az) % 360)

    # Day-of-year values for equinoxes and solstices
    season_days = [80, 172, 266, 355]
    lat_rad = math.radians(latitude)
    positions: List[SunPosition] = []
    for day in season_days:
        decl = math.radians(23.44) * math.sin(math.radians(360 / 365 * (day - 81)))
        # sunset hour angle
        try:
            omega_s = math.acos(-math.tan(lat_rad) * math.tan(decl))
        except ValueError:
            # polar day/night guard
            omega_s = math.pi
        for i in range(samples_per_day):
            ha = -omega_s + (2 * omega_s) * i / (samples_per_day - 1)
            elev, az = _solar_position(lat_rad, decl, ha)
            if elev >= 0:

                # weight sunlight intensity by elevation; near-horizon sun adds less
                weight = max(0.0, math.sin(math.radians(elev)))
                positions.append(
                    SunPosition(elevation=elev, azimuth=az, weight=weight)
                )
    return positions


def default_sun_positions(samples_per_day: int = 24) -> List[SunPosition]:
    """Sun positions for South Korea with a default sample count."""
    KOREA_LATITUDE = 37.5665  # Approximate latitude of Seoul, South Korea
    return sun_positions(KOREA_LATITUDE, samples_per_day)


def sun_vector(pos: SunPosition) -> Tuple[float, float, float]:
    # Return unit vector components (dx, dy, dz)
    elev_rad = math.radians(pos.elevation)
    azim_rad = math.radians(pos.azimuth)
    dx = math.cos(elev_rad) * math.sin(azim_rad)
    dy = math.cos(elev_rad) * math.cos(azim_rad)
    dz = math.sin(elev_rad)
    return dx, dy, dz
