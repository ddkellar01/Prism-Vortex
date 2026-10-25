import asyncio
import json
from typing import Any
from pipelines.earth_engine_client import EarthEngineClient
from pipelines.flow_telemetry_client import FlowTelemetryClient
from pipelines.people_search_client import PeopleSearchClient


class DataFusionPipeline:
    """Aggregates disparate intelligence streams concurrently into a unified context payload."""

    def __init__(self):
        self.people_client = PeopleSearchClient()
        self.earth_client = EarthEngineClient()
        self.flow_client = FlowTelemetryClient()

    async def aggregate_nexus_stream(
        self, target_query: str, coords: list[float]
    ) -> str:
        """Executes concurrent requests to all data clients and returns a unified JSON payload."""
        people_task = self.people_client.fetch_records(target_query)
        earth_task = self.earth_client.fetch_telemetry(coords)
        flow_task = self.flow_client.fetch_process_logs(target_query)

        people_data, earth_data, flow_data = await asyncio.gather(
            people_task, earth_task, flow_task, return_exceptions=True
        )

        merged_context: dict[str, Any] = {
            "source_people_search": (
                people_data
                if not isinstance(people_data, Exception)
                else str(people_data)
            ),
            "source_geospatial_earth": (
                earth_data
                if not isinstance(earth_data, Exception)
                else str(earth_data)
            ),
            "source_workflow_flow": (
                flow_data
                if not isinstance(flow_data, Exception)
                else str(flow_data)
            ),
        }

        return json.dumps(merged_context, indent=2)
