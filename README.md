# Credit Risk Analytics Toolkit

**Mission:** Internal tool for Nova Credit's Solutions Engineering team to generate "Retro-Risk Reports" for enterprise prospects, quantifying the value of Cash Atlas™ underwriting model on prospect data.

## Overview
This CLI tool processes a prospect's historical portfolio of declined loans (CSV) and generates a professional PDF report highlighting revenue opportunities and customer segments they're missing. It replaces costly validation studies with fast, data-backed analysis.

## Key Features

### PDF Report Generation
The toolkit automatically generates professional, branded PDF reports that include:
- **Executive Summary:** High-level metrics and business impact
- **Portfolio Lift Analysis:** Visual charts showing potential approval increases
- **Revenue Opportunity:** Quantified value of newly approved loans
- **Customer Segment Insights:** Analysis of which segments would benefit most
- **Professional Formatting:** Clean, enterprise-ready presentation

The PDF reports are designed for direct sharing with prospects and stakeholders, providing compelling visual evidence of Cash Atlas™ value proposition.

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
    --output-file sample_output/ACME_Retro_Report.pdf \
    --prospect-name "ACME Financial"
```

### Output
The tool generates two types of output:

1. **Console Output:** Real-time processing status and final metrics
2. **PDF Report:** Professional report saved to the specified output path

#### Console Output Example
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

#### PDF Report Features
- **Branded Design:** Nova Credit styling and professional layout
- **Interactive Charts:** Visual representation of portfolio lift analysis
- **Executive Summary:** Key metrics and business impact highlights
- **Detailed Analysis:** Comprehensive breakdown of simulation results
- **Ready for Presentation:** Enterprise-grade formatting for stakeholder meetings
