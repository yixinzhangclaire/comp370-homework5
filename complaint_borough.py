#!/usr/bin/env python3

import argparse
import csv
from collections import Counter
from datetime import datetime


def parse_args():
    parser = argparse.ArgumentParser(
        description="Count complaint types per borough for a given creation date range."
    )

    parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="Input CSV file"
    )

    parser.add_argument(
        "-s",
        "--start",
        required=True,
        help="Start date in YYYY-MM-DD format"
    )

    parser.add_argument(
        "-e",
        "--end",
        required=True,
        help="End date in YYYY-MM-DD format"
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Optional output CSV file"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    start_date = datetime.strptime(args.start, "%Y-%m-%d")
    end_date = datetime.strptime(args.end, "%Y-%m-%d")

    counts = Counter()

    with open(args.input, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            try:
                created_date = datetime.strptime(
                    row["Created Date"],
                    "%m/%d/%Y %I:%M:%S %p"
                )
            except (ValueError, TypeError):
                continue

            if start_date.date() <= created_date.date() <= end_date.date():
                complaint_type = row["Complaint Type"].strip()
                borough = row["Borough"].strip()

                if complaint_type and borough:
                    counts[(complaint_type, borough)] += 1

    if args.output:
        outfile = open(args.output, "w", newline="", encoding="utf-8")
    else:
        import sys
        outfile = sys.stdout

    writer = csv.writer(outfile)
    writer.writerow(["complaint type", "borough", "count"])

    for (complaint_type, borough), count in sorted(counts.items()):
        writer.writerow([complaint_type, borough, count])

    if args.output:
        outfile.close()


if __name__ == "__main__":
    main()
