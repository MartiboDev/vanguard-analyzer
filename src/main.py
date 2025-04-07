import pandas as pd
from cash_transaction_report import get_report
from read_cash_transaction import read_latest_cash_transaction

def main():
    # Read the latest cash transaction report
    df = read_latest_cash_transaction()

    if df is None:
        print("No valid cash transaction report found.")
        return
    
    get_report(df)

    
if __name__ == "__main__":
    main()