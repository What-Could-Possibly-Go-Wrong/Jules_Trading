import os
import pandas as pd
import argparse

# Get the absolute path of the project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def calculate_moving_averages(directory="Normierte Kurse", output_directory="Indikatoren"):
    """
    Calculates the 20-day and 100-day moving averages for each ticker.
    """
    dir_path = os.path.join(PROJECT_ROOT, directory)
    output_dir_path = os.path.join(PROJECT_ROOT, output_directory)

    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)

    for filename in os.listdir(dir_path):
        if filename.endswith(".csv"):
            filepath = os.path.join(dir_path, filename)
            df = pd.read_csv(filepath, index_col='Date', parse_dates=True)

            df['MA20'] = df['Normalized Close'].rolling(window=20).mean()
            df['MA100'] = df['Normalized Close'].rolling(window=100).mean()

            # Save the indicators
            output_filepath = os.path.join(output_dir_path, filename)
            df.index = df.index.strftime('%Y%m%d')
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