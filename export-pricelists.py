"""
reCarpet B2B — SparkLayer Price List Exporter
----------------------------------------------
Run this script after updating prices in reCarpet-pricelists-master.xlsx.
It generates 8 CSV files ready to upload to SparkLayer.

Usage:
    python export-pricelists.py

Output: sparklayer-pricelists/ folder (8 CSV files)
"""

import os
import csv
from openpyxl import load_workbook

EXCEL_FILE = "reCarpet-pricelists-master.xlsx"
OUTPUT_DIR = "sparklayer-pricelists"

# Map: (csv_filename, source_sheet, currency_key)
# currency_key: "sek" | "nok" | "dkk" | "eur"
EXPORTS = [
    ("sparklayer-entrepreneur-sek.csv", "Entrepreneur", "sek"),
    ("sparklayer-entrepreneur-nok.csv", "Entrepreneur", "nok"),
    ("sparklayer-entrepreneur-dkk.csv", "Entrepreneur", "dkk"),
    ("sparklayer-entrepreneur-eur.csv", "Entrepreneur", "eur"),
    ("sparklayer-member-sek.csv",       "Members",      "sek"),
    ("sparklayer-member-nok.csv",       "Members",      "nok"),
    ("sparklayer-member-dkk.csv",       "Members",      "dkk"),
    ("sparklayer-member-eur.csv",       "Members",      "eur"),
]

DATA_START_ROW = 5  # Row where SKU data begins in Entrepreneur/Members sheets


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(script_dir, EXCEL_FILE)
    output_dir = os.path.join(script_dir, OUTPUT_DIR)
    os.makedirs(output_dir, exist_ok=True)

    print(f"Reading: {EXCEL_FILE}")
    wb = load_workbook(excel_path, data_only=True)

    # Read exchange rates directly from the Exchange Rates sheet
    ws_rates = wb["Exchange Rates"]
    rates = {
        "sek": 1.0,
        "nok": ws_rates.cell(row=4, column=3).value,  # NOK rate
        "dkk": ws_rates.cell(row=5, column=3).value,  # DKK rate
        "eur": ws_rates.cell(row=6, column=3).value,  # EUR rate
    }
    print(f"  Rates — NOK: {rates['nok']}, DKK: {rates['dkk']}, EUR: {rates['eur']}")

    for csv_filename, sheet_name, currency in EXPORTS:
        ws = wb[sheet_name]
        rows_written = 0
        csv_path = os.path.join(output_dir, csv_filename)
        rate = rates[currency]

        with open(csv_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["sku", "quantity", "price"])

            row = DATA_START_ROW
            while True:
                sku   = ws.cell(row=row, column=1).value
                qty   = ws.cell(row=row, column=2).value
                sek   = ws.cell(row=row, column=3).value  # SEK is always a hardcoded value

                if sku is None:
                    break

                price = round(float(sek) * rate, 2)
                writer.writerow([sku, qty, f"{price:.2f}"])
                rows_written += 1
                row += 1

        print(f"  ✓  {csv_filename}  ({rows_written} rows)")

    print(f"\nDone — {len(EXPORTS)} files saved to '{OUTPUT_DIR}/'")
    print("Upload each file to the matching SparkLayer price list.")


if __name__ == "__main__":
    main()
