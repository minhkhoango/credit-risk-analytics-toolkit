# src/ingestion.py
"""
Handles loading and validating the prospect's portfolio CSV data.
"""

import csv
from pathlib import Path
from typing import List

from pydantic import BaseModel, Field, ValidationError


class LoanApplicationRecord(BaseModel):
    """
    Defines the data structure and validation rules for a single
    loan application record from the input CSV.
    """

    application_id: str = Field(..., min_length=1)
    loan_amount: float = Field(..., gt=0)
    stated_income: float = Field(..., gt=0)
    debt_to_income_ratio: float = Field(..., ge=0)


def load_and_validate_csv(file_path: Path) -> List[LoanApplicationRecord]:
    """
    Loads a CSV file from the given path and validates each row
    against the LoanApplicationRecord schema.

    Args:
        file_path: The path to the input CSV file.

    Returns:
        A list of validated LoanApplicationRecord objects.

    Raises:
        FileNotFoundError: If the file_path does not exist.
        ValueError: If the CSV contains validation errors.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Input file not found at: {file_path}")

    records: List[LoanApplicationRecord] = []
    try:
        with open(file_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                try:
                    # Pydantic automatically handles string -> float conversion
                    record = LoanApplicationRecord(**row)  # type: ignore
                    records.append(record)
                except ValidationError as e:
                    # Provide a user-friendly error pointing to the exact row
                    row_num = i + 2
                    error_msg = f"Validation error in CSV row {row_num}: {e}"
                    raise ValueError(error_msg) from e
    except Exception as e:
        # Catch other potential file reading errors
        raise IOError(f"Failed to read or process CSV file: {e}") from e

    if not records:
        raise ValueError("CSV file is empty or contains no valid data rows.")

    return records
