# Project Killshot: Credit Risk Analytics Toolkit

**Mission:** To build a high-impact, internal tool that allows Nova Credit's Solutions Engineering team to produce a "Retro-Risk Report" for enterprise prospects, dramatically shortening the sales cycle by quantifying the value of the Cash Atlas™ underwriting model on the prospect's own data.

**Overview**
This repository contains the "Concierge MVP" for the Validation Suite. This is not a customer-facing product but a powerful internal tool. It takes a prospect's historical portfolio of declined loans (as a CSV file) and generates a professional, data-driven PDF report that highlights the precise revenue and customer segments they are missing.
This tool is the "painkiller" for the "Underwriter's Dilemma"—it replaces a costly, months-long validation study with a fast, data-backed analysis, turning skepticism into urgency.

---

### Security & Data Handling: A Pre-Mortem

Security is not an afterthought; it is the foundation of this tool's credibility. The following outlines the data handling workflow, designed to meet the rigorous standards of a Tier-1 fintech environment.

#### 1. The Principle of Least Privilege
The architecture is designed to minimize its security footprint by design.

* **No Public-Facing Infrastructure:** The tool is a CLI script, not a web server. It has no open ports and no public attack surface.
* **No Persistent Datastores:** The script processes data in-memory and is designed to be stateless. It does not connect to or require a database.
* **No Customer UI:** By eliminating a self-service portal, we eliminate all risks associated with user authentication, session management, and web application vulnerabilities.

#### 2. Proposed Secure Data Handling Workflow
* **Data Ingestion:** The customer prospect will be provisioned access to a specific, segregated folder on an existing corporate SFTP server. This is the sole entry point for data.
* **Data In-Transit:** All data transfer over SFTP is secured with end-to-end encryption (e.g., SSH File Transfer Protocol).
* **Data At-Rest:** The CSV file is protected by the existing at-rest encryption and access control policies of the corporate file server.
* **Processing:** A credentialed Solutions Engineer, on a corporate-managed device, will pull the file to their local machine for processing. The script runs locally. The script does not need to access any other internal systems or APIs.
* **Data Purge Policy:** The input CSV file must be securely deleted from both the SFTP server and the local machine within 24 hours of the Retro-Risk Report.pdf being successfully generated and delivered. This is a critical data minimization step.

#### 3. Key Security Considerations
* **Personally Identifiable Information (PII):** The process requires that the prospect provide an anonymized or tokenized dataset. The `RUNBOOK.md` (to be created in Sprint 2) will contain explicit instructions on how to prepare the data.
* **Dependency Management:** The project uses poetry to lock dependencies, ensuring deterministic and secure builds. Regular vulnerability scanning via Snyk or Dependabot is recommended.

---

### Getting Started (Sprint 1)

This project uses Poetry for dependency management.

#### 1. Installation
First, ensure you have Python 3.11+ and Poetry installed. Then, from the project root:
```bash
# Install the project dependencies from the lock file
poetry install
```

#### 2. Running the Simulation
The Sprint 1 goal is to run the core simulation engine via the command-line interface and see the analytical results printed to the console.

A sample data file is provided at sample_data/sample_portfolio.csv.
```bash
# Run the simulation on the sample portfolio
poetry run python -m src.main process-portfolio \
    --input-file sample_data/sample_portfolio.csv \
    --prospect-name "ACME Financial"
```

#### 3. Expected Output
After running the command, you should see a dictionary printed to your console with the results of the analysis, similar to this:
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
