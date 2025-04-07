import os
from datetime import datetime
import pandas as pd

REPORT_DIR = "../reports"
OUTPUTS_DIR = "../outputs"

def read_latest_cash_transaction():
    """
    Reads the latest cash transaction report from a specified directory and returns it as a cleaned DataFrame.
    """
    # Check if the directory exists
    if not os.path.exists(REPORT_DIR):
        print(f"Error: Directory '{REPORT_DIR}' does not exist.")
        return None

    # Get a list of all files in the directory
    files = os.listdir(REPORT_DIR)

    # Filter files that start with 'cash-transaction-report' and match the date format
    report_files = []
    for f in files:
        if f.startswith('cash-transaction-report') and len(f) > 23:
            date_str = f[24:34]  # Extract the date part
            try:
                # Validate and parse the date format
                report_date = datetime.strptime(date_str, "%Y-%m-%d")
                # Append a tuple of (parsed date, filename) to the list
                report_files.append((report_date, f))
            except ValueError:
                # Skip files with invalid date formats
                continue

    # Sort files by date in descending order
    report_files.sort(key=lambda x: x[0], reverse=True)

    # Extract the filename of the latest report
    latest_report = report_files[0][1] if report_files else None

    if latest_report:
        # Construct the full path to the latest report
        latest_report_path = os.path.join(REPORT_DIR, latest_report)

        try:
            # Read the file into a DataFrame
            df = pd.read_csv(latest_report_path)

            # Drop unnecessary columns
            df = df.drop(columns=["Product type", "Product name"])

            # Rename columns
            df = df.rename(columns={"units": "Units", "Product ID": "Product"})

            # Drop rows with all NaN values
            df = df.dropna(how='all')

            # Save the cleaned DataFrame to a new file in the outputs directory
            output_dir = os.path.join(OUTPUTS_DIR)
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, f"cleaned_{latest_report}")
            df.to_csv(output_file, index=False)

            return df
        except Exception as e:
            print(f"Error reading the file '{latest_report}': {e}")
            return None
    else:
        print("No valid cash transaction reports found.")
        return None