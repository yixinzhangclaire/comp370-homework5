import csv
from collections import defaultdict
from datetime import datetime

input_file = "../311_2024_zip.csv"
output_file = "monthly_response_times.csv"

totals = defaultdict(float)
counts = defaultdict(int)
overall_totals = defaultdict(float)
overall_counts = defaultdict(int)

with open(input_file, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        created = row["Created Date"].strip()
        closed = row["Closed Date"].strip()
        zipcode = row["Incident Zip"].strip()

        if not created or not closed or not zipcode:
            continue

        if len(zipcode) != 5 or not zipcode.isdigit():
            continue

        try:
            created_dt = datetime.strptime(
                created,
                "%m/%d/%Y %I:%M:%S %p"
            )
            closed_dt = datetime.strptime(
                closed,
                "%m/%d/%Y %I:%M:%S %p"
            )
        except ValueError:
            continue

        response_hours = (closed_dt - created_dt).total_seconds() / 3600

        if response_hours < 0:
            continue

        month = closed_dt.strftime("%Y-%m")

        key = (zipcode, month)

        totals[key] += response_hours
        counts[key] += 1
        overall_totals[month] += response_hours
        overall_counts[month] += 1

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow([
        "zipcode",
        "month",
        "average_response_hours",
        "count"
    ])

    for key in sorted(totals):
        zipcode, month = key
        average = totals[key] / counts[key]

        writer.writerow([
            zipcode,
            month,
            average,
            counts[key]
        ])

    for month in sorted(overall_totals):
        average = overall_totals[month] / overall_counts[month]

        writer.writerow([
            "ALL",
            month,
            average,
            overall_counts[month]
        ])


print(f"Wrote {output_file}")
