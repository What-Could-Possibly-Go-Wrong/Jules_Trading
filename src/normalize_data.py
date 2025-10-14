import os
import pandas as pd
import argparse

def normalize_data(directory="Kurse", output_directory="Normierte Kurse"):
    """
    Normalizes the price data for each ticker.
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(directory, filename)
            df = pd.read_csv(filepath, index_col='Date', parse_dates=True)

            # Convert index to YYYYMMDD string format for comparison
            df.index = df.index.strftime('%Y%m%d')

            # Find the first trading day on or after 2000-01-01
            start_date = '20000101'
            first_day = df.index[df.index >= start_date].min()

            if pd.isna(first_day):
                print(f"Skipping {filename}: No data available on or after 2000-01-01.")
                continue

            # Normalize the 'Close' price
            base_price = df.loc[first_day, 'Close']
            if base_price == 0:
                print(f"Skipping {filename}: Base price is zero.")
                continue

            df['Normalized Close'] = 100 * (df['Close'] / base_price)

            # Save the normalized data
            output_filepath = os.path.join(output_directory, filename)
            df[['Normalized Close']].to_csv(output_filepath)
            print(f"Normalized data for {filename} and saved to {output_filepath}")

def main():
    parser = argparse.ArgumentParser(description="Normalize stock price data.")
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug logging.')
    args = parser.parse_args()

    if args.debug:
        print("Debug mode enabled.")

    normalize_data()

if __name__ == "__main__":
    main()