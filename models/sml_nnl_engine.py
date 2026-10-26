import torch
from torch import nn


class PrismNeuralScorer(nn.Module):
    """Local Neural Network Layer (NNL) for real-time edge scoring."""

    def __init__(self, input_dim: int = 10):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.Sigmoid(),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)


class EdgeScoringEngine:
    """Interface to run PyTorch inference on ingested feature vectors."""

    def __init__(self, input_dim: int = 10):
        self.model = PrismNeuralScorer(input_dim=input_dim)
        self.model.eval()

    def compute_risk(self, feature_vector: list[float]) -> float:
        """Executes tensor forward pass and returns scalar threat probability."""
        with torch.no_grad():
            input_tensor = torch.tensor([feature_vector], dtype=torch.float32)
            prediction = self.model(input_tensor)
            return round(prediction.item(), 4)