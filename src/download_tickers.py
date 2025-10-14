import requests
from bs4 import BeautifulSoup
import os
import argparse
import traceback

# Get the absolute path of the project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_sp500_tickers(debug=False):
    """
    Scrapes the S&P 500 ticker symbols from Wikipedia.
    """
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    html_content = response.text

    if debug:
        with open(os.path.join(PROJECT_ROOT, "sp500_debug.html"), "w", encoding="utf-8") as f:
            f.write(html_content)

    soup = BeautifulSoup(html_content, 'html.parser')

    table = soup.find('table', {'id': 'constituents'})
    if not table:
        raise ValueError("Could not find the S&P 500 constituents table with id 'constituents'. Check sp500_debug.html for the page structure.")

    tickers = []
    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')
        if not cells:
            continue
        ticker_cell = cells[0]
        ticker_link = ticker_cell.find('a')
        if ticker_link:
            ticker = ticker_link.text.strip()
            ticker = ticker.replace('.', '-')
            tickers.append(ticker)
    return tickers

def get_dax_tickers(debug=False):
    """
    Scrapes the DAX ticker symbols from Wikipedia.
    """
    url = "https://en.wikipedia.org/wiki/DAX"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    html_content = response.text

    if debug:
        with open(os.path.join(PROJECT_ROOT, "dax_debug.html"), "w", encoding="utf-8") as f:
            f.write(html_content)

    soup = BeautifulSoup(html_content, 'html.parser')

    table = soup.find('table', {'id': 'constituents'})
    if not table:
         raise ValueError("Could not find the DAX constituents table with id 'constituents'. Check dax_debug.html for the page structure.")

    tickers = []
    for row in table.find_all('tr')[1:]:
        # Ticker is in the 3rd column (index 2)
        cells = row.find_all('td')
        if len(cells) > 3:
            ticker = cells[3].text.strip()
            tickers.append(ticker)
    return tickers

def save_tickers(tickers, filename, directory="Ticker"):
    """
    Saves a list of tickers to a file.
    """
    dir_path = os.path.join(PROJECT_ROOT, directory)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    filepath = os.path.join(dir_path, filename)
    with open(filepath, 'w') as f:
        for ticker in tickers:
            f.write(f"{ticker}\n")
    print(f"Saved {len(tickers)} tickers to {filepath}")

def main():
    parser = argparse.ArgumentParser(description="Download stock tickers for S&P 500 and DAX.")
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug logging and save HTML content.')
    args = parser.parse_args()

    debug_filepath = os.path.join(PROJECT_ROOT, "debug.txt")

    if os.path.exists(debug_filepath):
        os.remove(debug_filepath)

    if args.debug:
        print("Debug mode enabled.")

    print("Downloading S&P 500 tickers...")
    try:
        sp500_tickers = get_sp500_tickers(args.debug)
        save_tickers(sp500_tickers, "sp500.txt")
        print("S&P 500 tickers downloaded successfully.")
    except Exception as e:
        print(f"Error downloading S&P 500 tickers: {e}")
        if args.debug:
            with open(debug_filepath, "a") as f:
                f.write(f"Error in get_sp500_tickers: {e}\n")
                f.write(traceback.format_exc())

    print("Downloading DAX tickers...")
    try:
        dax_tickers = get_dax_tickers(args.debug)
        save_tickers(dax_tickers, "dax.txt")
        print("DAX tickers downloaded successfully.")
    except Exception as e:
        print(f"Error downloading DAX tickers: {e}")
        if args.debug:
            with open(debug_filepath, "a") as f:
                f.write(f"Error in get_dax_tickers: {e}\n")
                f.write(traceback.format_exc())

if __name__ == "__main__":
    main()