import argparse
from src.download_tickers import main as download_tickers_main
from src.download_data import main as download_data_main
from src.normalize_data import main as normalize_data_main
from src.calculate_indicators import main as calculate_indicators_main
from src.trading_strategy import main as trading_strategy_main

def main():
    parser = argparse.ArgumentParser(description="Run the entire Jules Trading pipeline.")
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug logging.')
    args = parser.parse_args()

    print("--- Starting Jules Trading Pipeline ---")

    print("\nStep 1: Downloading Tickers...")
    download_tickers_main()

    print("\nStep 2: Downloading Data...")
    download_data_main()

    print("\nStep 3: Normalizing Data...")
    normalize_data_main()

    print("\nStep 4: Calculating Indicators...")
    calculate_indicators_main()

    print("\nStep 5: Running Trading Strategy...")
    trading_strategy_main()

    print("\n--- Jules Trading Pipeline Complete ---")

if __name__ == "__main__":
    main()