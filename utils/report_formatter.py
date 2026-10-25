import json
from datetime import datetime, timezone


class ReportFormatter:
    """Synthesizes agent reasoning into structured Markdown and JSON reports."""

    @staticmethod
    def format_agent_response(
        target_query: str,
        coordinates: list[float],
        risk_score: float,
        agent_raw_reasoning: str
    ) -> dict:
        """Packages scouting outputs into structured JSON payload."""
        timestamp = datetime.now(timezone.utc).isoformat()

        return {
            "metadata": {
                "system": "PrismVortex Engine",
                "timestamp": timestamp,
                "target_identifier": target_query,
                "coordinates": coordinates
            },
            "evaluation": {
                "neural_risk_score": risk_score,
                "threat_level": "CRITICAL" if risk_score > 0.75 else ("HIGH" if risk_score > 0.5 else "NORMAL")
            },
            "scout_analysis": agent_raw_reasoning
        }

    @staticmethod
    def to_markdown(report_data: dict) -> str:
        """Renders report dictionary into clean Markdown format."""
        meta = report_data["metadata"]
        eval_data = report_data["evaluation"]

        return f"""# PrismVortex Operational Threat Report
**Timestamp:** {meta['timestamp']}  
**Target Identifier:** `{meta['target_identifier']}`  
**Target Coordinates:** `{meta['coordinates']}`  
**Neural Risk Score:** `{eval_data['neural_risk_score']}` (**{eval_data['threat_level']}**)

---

## Agent Scout Analysis & Remediation
{report_data['scout_analysis']}
"""
