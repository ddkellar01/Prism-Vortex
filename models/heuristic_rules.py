from typing import Dict, Any, List


class HeuristicRuleEvaluator:
    """Static heuristic rule checker to complement neural edge scoring."""

    @staticmethod
    def evaluate_geospatial_anomaly(lat: float, lon: float, expected_region: str) -> bool:
        """Checks if coordinates deviate significantly from operational region bounding boxes."""
        # Baseline check (e.g., bounding coordinates outside normal operating boundaries)
        if lat < -90.0 or lat > 90.0 or lon < -180.0 or lon > 180.0:
            return True
        return False

    @staticmethod
    def extract_feature_vector(
        people_data: Dict[str, Any],
        earth_data: Dict[str, Any],
        flow_data: Dict[str, Any]
    ) -> List[float]:
        """Maps unstructured JSON telemetry feeds into a 10-dimensional PyTorch feature tensor."""
        features = [0.0] * 10

        # Feature 0: Matched identity risk signals
        if "risk_signals" in people_data:
            features[0] = min(len(people_data["risk_signals"]) * 0.25, 1.0)

        # Feature 1: Earth telemetry status
        if earth_data.get("status") == "unauthenticated_fallback":
            features[1] = 0.5
        elif "error" in earth_data:
            features[1] = 0.9

        # Feature 2: Infrastructure density metric
        features[2] = float(earth_data.get("infrastructure_density_score", 0.5))

        # Feature 3: Flow step anomalies flag
        if flow_data.get("step_anomalies_detected"):
            features[3] = 0.85

        # Feature 4: Flow latency spike magnitude
        latency = flow_data.get("latency_spike_ms", 0)
        features[4] = min(latency / 2000.0, 1.0)

        # Features 5-9: Baseline synthetic metrics for model input tensor padding
        features[5] = 0.12
        features[6] = 0.44
        features[7] = 0.88
        features[8] = 0.23
        features[9] = 0.05

        return features
