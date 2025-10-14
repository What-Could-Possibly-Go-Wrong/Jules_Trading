# Jules Trading

This project is a platform for testing various trading strategies using Python. The focus is on readability, simplicity, and maintainability.

## Features

*   **Ticker Management**: Downloads and manages stock tickers for different indices.
*   **Data Handling**: Fetches and updates historical price data for stocks.
*   **Data Normalization**: Normalizes price data for comparability.
*   **Indicator Calculation**: Computes technical indicators like moving averages.
*   **Strategy Simulation**: Backtests trading strategies with historical data.
*   **Evaluation**: Provides tools to analyze the performance of trading strategies.
*   **Debugging**: Includes extensive debugging options via a `-d` parameter.

## Project Structure

*   `Ticker/`: Contains lists of stock tickers.
*   `Kurse/`: Stores raw historical price data.
*   `Normierte Kurse/`: Stores normalized price data.
*   `Indikatoren/`: Contains calculated technical indicators.
*   `Trading/`: Holds the trading strategy logic and results.
*   `src/`: Contains the main source code.
*   `tests/`: Contains tests for the project.
*   `debug.txt`: Logs debugging information.
*   `Feedback.txt`: Collects suggestions for improvements.

## How to Run

1.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
2.  Run the scripts in the following order:
    ```bash
    python src/download_tickers.py
    python src/download_data.py
    python src/normalize_data.py
    python src/calculate_indicators.py
    python src/trading_strategy.py
    ```
3.  To run the tests:
    ```bash
    python -m unittest discover tests
    ```