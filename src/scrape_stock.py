import requests
from bs4 import BeautifulSoup

def get_stock_price(ticker, market="AX"):
    """
    Fetch the current stock price for the given ticker from Yahoo Finance.
    
    Args:
        ticker (str): The stock ticker symbol (e.g., "VGS.AX").
    
    Returns:
        str: The current stock price as a string, or an error message if not found.
    """
    url = f"https://au.finance.yahoo.com/quote/{ticker}.{market}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        # Send a GET request to the Yahoo Finance page
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the stock price element
        price_element = soup.find('span', {'data-testid': 'qsp-price'})
        if price_element:
            try:
                return float(price_element.text.strip().replace(',', ''))
            except ValueError:
                return 0.0
        else:
            return 0.0

    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"