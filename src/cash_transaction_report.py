from colorama import Fore, Style
import pandas as pd
from scrape_stock import get_stock_price

def get_report(df):
    """
    Process a cleaned DataFrame to generate a cash transaction report.
    """
    print(Fore.GREEN + "Generating cash transaction report..." + Style.RESET_ALL)

    stock_holdings_df = get_stock_holdings(df)
    cash_holdings_df = get_cash_holdings(df)
    dividend_payments_df = get_dividend_payments(df)
    portfolio_value = get_portfolio_value(cash_holdings_df, stock_holdings_df)
    
    print(Fore.MAGENTA + "\nCash Holdings:" + Style.RESET_ALL)
    print(cash_holdings_df)

    print(Fore.CYAN + "\nStock Holdings:" + Style.RESET_ALL)
    print(stock_holdings_df)

    print(Fore.YELLOW + "\nDividend Payments:" + Style.RESET_ALL)
    print(dividend_payments_df)

    print(Fore.RED + "\nPortfolio Value:" + Style.RESET_ALL)
    print(portfolio_value)
    
    return df

def get_cash_holdings(df):
    """
    Process the DataFrame to calculate cash holdings.
    Outputs a DataFrame with 'Product', 'Total', 'Total In', and 'Total Out' columns.
    """
    # Calculate total deposited (positive values)
    total_in = df[df['Type'] == 'Deposit']['Total'].sum()

    # Calculate total withdrawn (negative values)
    total_out = df[df['Type'] == 'Withdrawal']['Total'].sum()

    # Sum the 'Total' column for cash transactions
    total_cash = df['Total'].sum()

    # Create a new DataFrame with the cash product and its values
    df = pd.DataFrame({
        'Product': ['Cash'],
        'Total In': [total_in],
        'Total Out': [abs(total_out)],
        'Current Balance': [total_cash]
    })

    return df

def get_stock_holdings(df):
    """
    Process the DataFrame to calculate current stock holdings.
    Outputs a DataFrame with 'Product', 'Units', 'Total Cost', 'Avg Unit Cost', and 'Total Value' columns.
    """
    # Map 'Buy' to positive and 'Sell' to negative units
    df['Units'] = df.apply(lambda row: row['Units'] if row['Type'] == 'Buy' else -row['Units'], axis=1)
    df['Total Cost'] = df.apply(lambda row: -row['Total'] if row['Type'] == 'Buy' else row['Total'], axis=1)

    # Group by 'Product' and sum the 'Units' and 'Total Cost' columns
    df = df.groupby('Product', as_index=False).agg({'Units': 'sum', 'Total Cost': 'sum'})

    # Filter out products with zero or negative units (if needed)
    df = df[df['Units'] > 0]

    # Add "Avg Unit Cost" column
    df['Avg Unit Cost'] = df['Total Cost'] / df['Units']

    # Reorder columns so "Avg Unit Cost" is before "Total Cost"
    df = df[['Product', 'Units', 'Avg Unit Cost', 'Total Cost']]

    # Add "Unit Value" and "Total Value" columns
    df['Unit Value'] = df['Product'].apply(get_stock_price)
    df['Total Value'] = df['Units'] * df['Unit Value']

    # Add "Portfolio Percentage" column based on "Total Value"
    total_portfolio_value = df['Total Value'].sum()
    df['Portfolio Percentage'] = (df['Total Value'] / total_portfolio_value) * 100

    # Reset the index to ensure it starts at 0
    df = df.reset_index(drop=True)

    return df

def get_dividend_payments(df):
    """
    Process the DataFrame to calculate dividend payments.
    Outputs a DataFrame with 'Product' and 'Dividend' columns.
    """
    # Filter for dividend transactions
    df = df[df['Type'] == 'Distribution']

    # Group by 'Product' and sum the 'Dividend' column
    df = df.groupby('Type')['Total'].sum().reset_index()

    return df

def get_portfolio_value(cash_holdings_df, stock_holdings_df):
    """
    Calculate the total portfolio value from cash and stock holdings.
    """
    # Get the total cash value
    total_in = cash_holdings_df['Total In'].sum()
    total_out = cash_holdings_df['Total Out'].sum()
    total_cash = cash_holdings_df['Current Balance'].sum()

    # Get the total stock value
    total_stock_cost = stock_holdings_df['Total Cost'].sum()
    total_stock = stock_holdings_df['Total Value'].sum()

    # Get the total portfolio value
    portfolio_cost = total_in - total_out
    portfolio_value = total_cash + total_stock
    portfolio_gain = portfolio_value - portfolio_cost
    portfolio_percentage_diff = (portfolio_value / portfolio_cost - 1) * 100

    df = pd.DataFrame({
        'Cost': [portfolio_cost],
        'Value': [portfolio_value],
        'Gain': [portfolio_gain],
        'Percentage Diff': [portfolio_percentage_diff]
    })

    return df