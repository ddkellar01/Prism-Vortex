import pytest

from pipelines.fusion_pipeline import DataFusionPipeline


@pytest.mark.asyncio
async def test_data_fusion_aggregation():
    """Validates concurrent aggregation across identity, geospatial, and workflow sources."""
    pipeline = DataFusionPipeline()
    target_query = "Test_Target_Alpha"
    coords = [37.7749, -122.4194]

    result_json_str = await pipeline.aggregate_nexus_stream(target_query, coords)

    assert result_json_str is not None
    assert "source_people_search" in result_json_str
    assert "source_geospatial_earth" in result_json_str
    assert "source_workflow_flow" in result_json_str
    assert target_query in result_json_str
    