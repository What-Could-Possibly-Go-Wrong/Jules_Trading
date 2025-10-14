import os
import pandas as pd
import numpy as np
import argparse
from scipy.stats import gmean

# Get the absolute path of the project root by finding the 'src' directory
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(PROJECT_ROOT) == 'src':
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)


def calculate_kpis(df, trade_log, start_capital):
    """
    Calculates and returns a dictionary of Key Performance Indicators (KPIs).
    """
    final_value = df['portfolio_value'].iloc[-1]
    total_return = (final_value / start_capital) - 1

    # Calculate annualized return
    days = (df.index[-1] - df.index[0]).days
    if days == 0:
        annualized_return = 0
    else:
        annualized_return = (1 + total_return) ** (365.0 / days) - 1

    # Calculate Sharpe Ratio
    df['daily_return'] = df['portfolio_value'].pct_change()
    if df['daily_return'].std() == 0:
        sharpe_ratio = 0
    else:
        sharpe_ratio = df['daily_return'].mean() / df['daily_return'].std() * np.sqrt(252)

    # Calculate Max Drawdown
    df['peak'] = df['portfolio_value'].cummax()
    df['drawdown'] = (df['portfolio_value'] - df['peak']) / df['peak']
    max_drawdown = df['drawdown'].min()

    return {
        "Total Return": f"{total_return:.2%}",
        "Annualized Return": f"{annualized_return:.2%}",
        "Sharpe Ratio": f"{sharpe_ratio:.2f}",
        "Max Drawdown": f"{max_drawdown:.2%}",
        "Final Portfolio Value": f"{final_value:.2f}"
    }

def run_gld_20_100_strategy(ticker, start_capital=10000, kurse_dir="Kurse", indikatoren_dir="Indikatoren", trading_dir="Trading"):
    """
    Runs the GLD 20-100 trading strategy for a single ticker.
    """
    trading_dir_path = os.path.join(PROJECT_ROOT, trading_dir)
    if not os.path.exists(trading_dir_path):
        os.makedirs(trading_dir_path)

    kurse_filepath = os.path.join(PROJECT_ROOT, kurse_dir, f"{ticker}.csv")
    indikatoren_filepath = os.path.join(PROJECT_ROOT, indikatoren_dir, f"{ticker}.csv")

    if not os.path.exists(kurse_filepath) or not os.path.exists(indikatoren_filepath):
        print(f"Skipping {ticker}: Missing data or indicator file.")
        print(f"Looked for: {kurse_filepath}")
        print(f"Looked for: {indikatoren_filepath}")
        return

    # Load data
    prices_df = pd.read_csv(kurse_filepath, index_col='Date', parse_dates=True)
    indicators_df = pd.read_csv(indikatoren_filepath, index_col='Date', parse_dates=True)

    # Combine dataframes
    df = pd.concat([prices_df, indicators_df], axis=1).dropna()
    df.index = pd.to_datetime(df.index, format='%Y%m%d')

    # Initialize variables
    cash = start_capital
    shares = 0
    trade_log = []
    df['portfolio_value'] = float(start_capital) # Initialize with float

    # Create a 'position' column
    df['position'] = np.where(df['MA20'] > df['MA100'], 1, 0)
    # Detect crossovers
    df['crossover'] = df['position'].diff()

    for i in range(1, len(df)):
        # Buy signal
        if df['crossover'].iloc[i] == 1:
            price = df['Open'].iloc[i]
            if cash > price:
                shares_to_buy = int(cash // price)
                cost = shares_to_buy * price
                cash -= cost
                shares += shares_to_buy
                trade_log.append(f"{df.index[i].strftime('%Y%m%d')}: BUY {shares_to_buy} shares of {ticker} at {price:.2f}")
        # Sell signal
        elif df['crossover'].iloc[i] == -1:
            if shares > 0:
                price = df['Open'].iloc[i]
                revenue = shares * price
                cash += revenue
                trade_log.append(f"{df.index[i].strftime('%Y%m%d')}: SELL {shares} shares of {ticker} at {price:.2f}")
                shares = 0
        df.loc[df.index[i], 'portfolio_value'] = cash + (shares * df['Close'].iloc[i])

    # Save the trade log
    log_filepath = os.path.join(trading_dir_path, f"{ticker}_tradelog.txt")
    with open(log_filepath, 'w') as f:
        for entry in trade_log:
            f.write(f"{entry}\n")

    kpis = calculate_kpis(df, trade_log, start_capital)

    print(f"\n--- Evaluation for {ticker} ---")
    for key, value in kpis.items():
        print(f"{key}: {value}")

    # Save KPIs to a file
    kpi_filepath = os.path.join(trading_dir_path, f"{ticker}_kpis.txt")
    with open(kpi_filepath, 'w') as f:
        for key, value in kpis.items():
            f.write(f"{key}: {value}\n")


def main():
    parser = argparse.ArgumentParser(description="Run trading strategies and evaluate performance.")
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug logging.')
    args = parser.parse_args()

    if args.debug:
        print("Debug mode enabled.")

    tickers_to_trade = []
    ticker_dir = os.path.join(PROJECT_ROOT, "Ticker")
    for ticker_file in ["sp500.txt", "dax.txt"]:
        filepath = os.path.join(ticker_dir, ticker_file)
        if not os.path.exists(filepath):
            print(f"Ticker file not found at {filepath}")
            continue
        with open(filepath, 'r') as f:
            tickers_to_trade.extend([line.strip() for line in f if line.strip()][:5])

    for ticker in tickers_to_trade:
        run_gld_20_100_strategy(ticker)

if __name__ == "__main__":
    main()