# Credit Risk Analytics Toolkit

**Mission:** Internal tool for Nova Credit's Solutions Engineering team to generate "Retro-Risk Reports" for enterprise prospects, quantifying the value of Cash Atlas™ underwriting model on prospect data.

## Overview
This CLI tool processes a prospect's historical portfolio of declined loans (CSV) and generates a professional PDF report highlighting revenue opportunities and customer segments they're missing. It replaces costly validation studies with fast, data-backed analysis.

## Security & Data Handling

### Architecture
- **CLI-based:** No web server, no open ports, no public attack surface
- **Stateless:** Processes data in-memory, no persistent datastores
- **Local processing:** Runs on credentialed Solutions Engineer's corporate device

### Data Workflow
1. **Ingestion:** Prospect uploads anonymized CSV to segregated SFTP folder
2. **Processing:** Solutions Engineer downloads and processes locally
3. **Purge:** Input file deleted within 24 hours of report generation

## Getting Started

### Prerequisites
- Python 3.11+
- Poetry

### Installation
```bash
poetry install
```

### Usage
```bash
poetry run python -m src.main \
    --input-file sample_data/sample_portfolio.csv \
    --prospect-name "ACME Financial"
```

### Expected Output
```json
{
    "prospect_name": "ACME Financial",
    "total_applications_processed": 5,
    "decisions_flipped_to_approve": 2,
    "potential_lift_percentage": 40.0,
    "total_value_of_newly_approved_loans": 60000.0,
    "average_loan_value_of_lifted_apps": 30000.0
}
```
