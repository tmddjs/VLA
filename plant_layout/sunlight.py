import math
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class SunPosition:
    elevation: float  # degrees above horizon
    azimuth: float    # degrees from north clockwise


def sun_positions(latitude: float, samples_per_day: int = 16) -> List[SunPosition]:
    """Calculate seasonal sun positions for a given latitude.

    Args:
        latitude: Latitude in degrees (positive north).
        samples_per_day: Number of time samples per simulated day.

    Returns:
        A list of :class:`SunPosition` objects containing sun elevation and
        azimuth angles for the four principal seasons. Positions where the sun
        is below the horizon are discarded.
    """

    def _solar_position(lat_deg: float, day_of_year: int, hour: float) -> Tuple[float, float]:
        """Compute solar elevation and azimuth for given inputs."""
        lat = math.radians(lat_deg)
        # Approximate solar declination angle (in radians)
        decl = math.radians(23.44) * math.sin(math.radians(360 / 365 * (day_of_year - 81)))
        # Hour angle (in radians), assuming local solar time
        hour_angle = math.radians(15 * (hour - 12))

        sin_elev = (
            math.sin(lat) * math.sin(decl)
            + math.cos(lat) * math.cos(decl) * math.cos(hour_angle)
        )
        elev = math.asin(sin_elev)

        cos_az = (
            math.sin(decl) - math.sin(elev) * math.sin(lat)
        ) / (math.cos(elev) * math.cos(lat))
        cos_az = max(-1.0, min(1.0, cos_az))  # guard against floating errors
        az = math.acos(cos_az)
        if math.sin(hour_angle) > 0:
            az = 2 * math.pi - az
        return math.degrees(elev), (math.degrees(az) % 360)

    # Day-of-year values for equinoxes and solstices
    season_days = [80, 172, 266, 355]
    positions: List[SunPosition] = []
    step = 24 / samples_per_day
    for day in season_days:
        for i in range(samples_per_day):
            hour = i * step
            elev, az = _solar_position(latitude, day, hour)
            if elev >= 0:  # filter positions below the horizon
                positions.append(SunPosition(elevation=elev, azimuth=az))
    return positions


def default_sun_positions(samples_per_day: int = 16) -> List[SunPosition]:
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
