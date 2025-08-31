# src/main.py
"""
The main entry point for the Command-Line Interface (CLI) of the
Credit Risk Analytics Toolkit.
"""

import json
from pathlib import Path
from typing import Optional

import typer

from .engine import RetroSimulationEngine
from .ingestion import load_and_validate_csv
from .modeling import MockCashAtlasModel

app = typer.Typer(
    name="Credit Risk Analytics Toolkit",
    help="An internal tool to run retro-risk simulations on prospect portfolios.",
)


@app.command()
def process_portfolio(
    input_file: Path = typer.Option(
        ...,
        "--input-file",
        "-i",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Path to the input CSV file with the prospect's portfolio.",
    ),
    prospect_name: str = typer.Option(
        ...,
        "--prospect-name",
        "-n",
        help="Name of the prospect company (e.g., 'ACME Financial').",
    ),
    output_file: Optional[Path] = typer.Option(
        None,  # In Sprint 2, this will be the path for the PDF
        "--output-file",
        "-o",
        help="Path to save the output report. (Ignored in Sprint 1)",
    ),
) -> None:
    """
    Loads, validates, and processes a loan portfolio CSV to generate a
    retro-risk analysis.
    """
    typer.echo(f"🚀 Starting analysis for prospect: {prospect_name}")
    typer.echo(f"   -> Loading data from: {input_file}")

    try:
        # 1. Ingestion & Validation
        records = load_and_validate_csv(input_file)
        typer.echo(f"✅ Data validation successful. Found {len(records)} records.")

        # 2. MOdeling & Simulation
        model = MockCashAtlasModel()
        engine = RetroSimulationEngine(model)
        results = engine.run_simulation(records)
        results[
            "prospect_name"
        ] = prospect_name  # Add prospect name to the final report

        typer.echo("✅ Simulation complete.")
        typer.echo("\n--- Simulation Results ---")

        # Pretty print the JSON results to the console
        typer.echo(json.dumps(results, indent=4))

        typer.echo("\n---")
        typer.echo("🏁 Sprint 1 Goal Achieved: Core engine ran successfully.")

    except (FileNotFoundError, ValueError, IOError) as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED, bold=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
