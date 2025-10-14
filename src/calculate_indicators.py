import os
import pandas as pd
import argparse

def calculate_moving_averages(directory="Normierte Kurse", output_directory="Indikatoren"):
    """
    Calculates the 20-day and 100-day moving averages for each ticker.
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(directory, filename)
            df = pd.read_csv(filepath, index_col='Date', parse_dates=True)

            df['MA20'] = df['Normalized Close'].rolling(window=20).mean()
            df['MA100'] = df['Normalized Close'].rolling(window=100).mean()

            # Save the indicators
            output_filepath = os.path.join(output_directory, filename)
            df[['MA20', 'MA100']].to_csv(output_filepath)
            print(f"Calculated indicators for {filename} and saved to {output_filepath}")

def main():
    parser = argparse.ArgumentParser(description="Calculate technical indicators.")
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug logging.')
    args = parser.parse_args()

    if args.debug:
        print("Debug mode enabled.")

    calculate_moving_averages()

if __name__ == "__main__":
    main()