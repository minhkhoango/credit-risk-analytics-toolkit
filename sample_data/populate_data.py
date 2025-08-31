import csv
import random

# The path to the CSV file to be populated
# The file path is relative to the project's root directory
csv_file_path = "sample_data/sample_portfolio.csv"

# Header for the CSV file
header = ["application_id", "loan_amount", "stated_income", "debt_to_income_ratio"]

# Generate 2000 rows of realistic data
with open(csv_file_path, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(header)
    for i in range(1, 2001):
        application_id = f"app-{i:03d}"
        loan_amount = random.randint(5000, 100000)
        stated_income = random.randint(30000, 250000)
        debt_to_income_ratio = round(random.uniform(0.1, 0.9), 2)
        writer.writerow(
            [application_id, loan_amount, stated_income, debt_to_income_ratio]
        )

print(f"Successfully populated '{csv_file_path}' with 2000 rows of data.")
