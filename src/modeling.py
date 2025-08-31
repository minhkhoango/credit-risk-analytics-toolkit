# src/modeling.py
"""
Defines the interface for underwriting models and provides a mock
implementation for development and testing.
"""

from typing import Protocol, TypedDict, Literal

from .ingestion import LoanApplicationRecord


class PredictionResult(TypedDict):
    """Result of an underwriting model prediction."""

    cash_flow_stability_score: float
    simulated_decision: Literal["APPROVE"] | Literal["DECLINE"]


class UnderwritingModelProtocol(Protocol):
    """
    A protocol defining the interface that all underwriting models must adhere to.
    This allows for interchangeable models (e.g., mock vs. real).
    """

    def predict(self, record: LoanApplicationRecord) -> PredictionResult:
        """
        Takes a loan application record and returns a prediction.

        Args:
            record: The loan application data.

        Returns:
            A typed dictionary containing the model's prediction, including a score
            and a decision.
        """
        ...


class MockCashAtlasModel:
    """
    A mock implementation of the Cash Atlas underwriting model.

    This serves as a stand-in for the real, complex model during development.
    The logic here is intentionally simple for demonstration purposes.
    """

    def predict(self, record: LoanApplicationRecord) -> PredictionResult:
        """
        Generates a synthetic "Cash Flow Stability Score" and makes a decision.

        The logic is simple: a higher score is given to applicants with a lower
        debt-to-income ratio and a higher income relative to their loan amount.
        """
        # A simple formula to generate a plausible score between 300 and 850
        income_to_loan_ratio = record.stated_income / record.loan_amount
        score = 300 + (income_to_loan_ratio * 100) - (record.debt_to_income_ratio * 200)
        score = max(300, min(850, score))  # Clamp score within a realistic range

        decision = "APPROVE" if score > 650 else "DECLINE"

        return {"cash_flow_stability_score": score, "simulated_decision": decision}
