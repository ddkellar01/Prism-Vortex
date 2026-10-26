from typing import Any

import ee

from config.settings import settings


class EarthEngineClient:
    """Interacts with Google Earth Engine for spatial terrain telemetry."""

    def __init__(self):
        self.initialized = False
        try:
            ee.Initialize(project=settings.EARTH_ENGINE_PROJECT)
            self.initialized = True
        except ee.EEException:
            # Unauthenticated / unconfigured Earth Engine access lands here
            # (verified: ee.Initialize raises EEException without credentials).
            self.initialized = False

    async def fetch_telemetry(self, coordinates: list[float]) -> dict[str, Any]:
        """Pulls spatial metrics surrounding given latitude and longitude."""
        if not coordinates or len(coordinates) < 2:
            return {"error": "Invalid coordinates supplied."}

        lat, lon = coordinates[0], coordinates[1]

        if not self.initialized:
            return {
                "latitude": lat,
                "longitude": lon,
                "status": "unauthenticated_fallback",
                "elevation_m": 120.5,
                "infrastructure_density_score": 0.82,
            }

        try:
            point = ee.Geometry.Point([lon, lat])
            return {
                "latitude": lat,
                "longitude": lon,
                "status": "authenticated",
                "point_buffer": point.buffer(100).toGeoJSON(),
            }
        except ee.EEException as e:
            return {"latitude": lat, "longitude": lon, "error": str(e)}