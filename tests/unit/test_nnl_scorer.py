from models.heuristic_rules import HeuristicRuleEvaluator
from models.sml_nnl_engine import EdgeScoringEngine


def test_edge_scoring_engine_forward_pass():
    """Validates that the PyTorch neural network layer returns a valid probability float."""
    engine = EdgeScoringEngine(input_dim=10)
    mock_features = [0.1, 0.5, 0.8, 0.2, 0.9, 0.3, 0.4, 0.7, 0.1, 0.6]

    risk_score = engine.compute_risk(mock_features)

    assert isinstance(risk_score, float)
    assert 0.0 <= risk_score <= 1.0


def test_feature_vector_extraction():
    """Validates mapping of raw JSON feeds to feature tensors."""
    people_data = {"risk_signals": ["anomaly_1", "anomaly_2"]}
    earth_data = {"status": "authenticated", "infrastructure_density_score": 0.75}
    flow_data = {"step_anomalies_detected": True, "latency_spike_ms": 1000}

    features = HeuristicRuleEvaluator.extract_feature_vector(
        people_data, earth_data, flow_data
    )

    assert len(features) == 10
    assert features[0] == 0.5  # 2 signals * 0.25
    assert features[2] == 0.75  # density score
    assert features[3] == 0.85  # anomaly flag
    assert features[4] == 0.5  # 1000 / 2000