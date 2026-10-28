from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

from agents.argon_core import ArgonAgentOrchestrator
from config.logging_config import logger, setup_logging
from config.settings import settings
from models.heuristic_rules import HeuristicRuleEvaluator
from models.sml_nnl_engine import EdgeScoringEngine
from pipelines.fusion_pipeline import DataFusionPipeline
from utils.report_formatter import ReportFormatter
from utils.security_sanitizer import SecuritySanitizer

setup_logging(level="INFO" if not settings.DEBUG else "DEBUG")

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Autonomous Multi-Agent Threat Scouting & Data Fusion Engine",
)

sanitizer = SecuritySanitizer()
fusion_pipeline = DataFusionPipeline()
scoring_engine = EdgeScoringEngine(input_dim=10)
agent_orchestrator = ArgonAgentOrchestrator()


class ScoutTargetRequest(BaseModel):
    target_identifier: str = Field(..., example="Facility_9_Gateway")
    coordinates: list[float] = Field(..., example=[34.0522, -118.2437])
    objective: str = Field(
        ...,
        example=(
            "Scout for perimeter threats, supply chain risks, and access" " anomalies."
        ),
    )


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health check endpoint for cluster readiness probes."""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
    }


@app.post("/v1/scout", status_code=status.HTTP_200_OK)
async def execute_scout_operation(payload: ScoutTargetRequest):
    """Primary REST endpoint to trigger an autonomous scouting operation."""
    try:
        clean_target = sanitizer.sanitize_text(payload.target_identifier)
        clean_objective = sanitizer.sanitize_text(payload.objective)

        logger.info(f"Starting PrismVortex scout operation for target: {clean_target}")

        raw_context_str = await fusion_pipeline.aggregate_nexus_stream(
            clean_target, payload.coordinates
        )

        import json

        parsed_context = json.loads(raw_context_str)
        features = HeuristicRuleEvaluator.extract_feature_vector(
            parsed_context.get("source_people_search", {}),
            parsed_context.get("source_geospatial_earth", {}),
            parsed_context.get("source_workflow_flow", {}),
        )
        local_risk_score = scoring_engine.compute_risk(features)

        raw_agent_analysis = agent_orchestrator.execute_deep_scout(
            objective=clean_objective,
            context_payload=raw_context_str,
            local_risk_score=local_risk_score,
        )

        formatted_report = ReportFormatter.format_agent_response(
            target_query=clean_target,
            coordinates=payload.coordinates,
            risk_score=local_risk_score,
            agent_raw_reasoning=raw_agent_analysis,
        )

        return formatted_report

    # Catch-all API boundary: any pipeline/agent failure becomes a 500.
    except Exception as err:
        logger.error(f"Uncaught exception during scouting operation: {err!s}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"PrismVortex execution failure: {err!s}",
        ) from err


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
    