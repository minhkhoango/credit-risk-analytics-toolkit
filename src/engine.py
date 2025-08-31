# src/engine.py
"""
The core simulation engine that processes a portfolio of loan applications
using a given underwriting model and calculates key metrics.
"""

from typing import List, NotRequired, TypedDict

from .ingestion import LoanApplicationRecord
from .modeling import UnderwritingModelProtocol


class SimulationResults(TypedDict):
    """Results of the retro-simulation process."""

    total_applications_processed: int
    decisions_flipped_to_approve: int
    potential_lift_percentage: float
    total_value_of_newly_approved_loans: float
    average_loan_value_of_lifted_apps: float
    prospect_name: NotRequired[str]


class RetroSimulationEngine:
    """
    Orchestrates the retro-simulation process.
    """

    def __init__(self, model: UnderwritingModelProtocol) -> None:
        """
        Initializes the engine with a specific underwriting model.

        Args:
            model: An object that conforms to the UnderwritingModelProtocol.
        """
        self._model = model

    def run_simulation(self, records: List[LoanApplicationRecord]) -> SimulationResults:
        """
        Runs the simulation on a list of loan application records.

        Args:
            records: A list of validated loan application records.

        Returns:
            A dictionary containing the aggregated results and key metrics
            of the simulation.
        """
        total_applications: int = len(records)
        flipped_decisions: int = 0
        total_value_of_flipped_loans: float = 0.0

        for record in records:
            prediction = self._model.predict(record)
            if prediction["simulated_decision"] == "APPROVE":
                flipped_decisions += 1
                total_value_of_flipped_loans += record.loan_amount

        lift_percentage: float = (
            (flipped_decisions / total_applications) * 100
            if total_applications > 0
            else 0
        )

        avg_loan_value: float = (
            total_value_of_flipped_loans / flipped_decisions
            if flipped_decisions > 0
            else 0
        )

        return {
            "total_applications_processed": total_applications,
            "decisions_flipped_to_approve": flipped_decisions,
            "potential_lift_percentage": round(lift_percentage, 2),
            "total_value_of_newly_approved_loans": round(
                total_value_of_flipped_loans, 2
            ),
            "average_loan_value_of_lifted_apps": round(avg_loan_value, 2),
        }
