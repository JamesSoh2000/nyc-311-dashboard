
import argparse
import pandas as pd

def parse_arguments():
    """Parse command-line arguments using argparse."""
    parser = argparse.ArgumentParser(
        description="Count complaint types per borough in a given date range."
    )
    parser.add_argument('-i', '--input', required=True, help="Path to the input CSV file.")
    parser.add_argument('-s', '--start', required=True, help="Start date (YYYY-MM-DD).")
    parser.add_argument('-e', '--end', required=True, help="End date (YYYY-MM-DD).")
    parser.add_argument('-o', '--output', help="Path to the output CSV file (optional).")


    return parser.parse_args()

def load_data(input_file, start_date, end_date):
    """Load and filter the data based on the given date range."""
    # Load the CSV without a header
    df = pd.read_csv(input_file, header=None)
    
    # Convert the first column (index 0, assumed to be 'Created Date') to datetime
    df[1] = pd.to_datetime(df[1])  # Assuming index 0 is 'Created Date'
    
    # Convert start and end dates from arguments
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Filter the dataframe for the date range using index 0 for 'Created Date'
    mask = (df[1] >= start_date) & (df[1] <= end_date)
    filtered_df = df[mask]
    
    return filtered_df

def count_complaints_by_borough(df):
    """Count the number of each complaint type per borough."""
    # Assuming index 1 is 'Complaint Type' and index 2 is 'Borough'
    complaint_counts = df.groupby([5, 25]).size().reset_index(name='Count')
    complaint_counts.columns = ['Complaint Type', 'Borough', 'Count']
    return complaint_counts

def output_results(complaint_counts, output_file=None):
    """Output the results in CSV format, either to stdout or to a file."""
    if output_file:
        complaint_counts.to_csv(output_file, index=False)
    else:
        print(complaint_counts.to_csv(index=False))

def main():
    """Main function to run the CLI tool."""
    args = parse_arguments()
    
    # Load and filter the dataset
    filtered_df = load_data(args.input, args.start, args.end)
    
    # Count complaints by borough and complaint type
    complaint_counts = count_complaints_by_borough(filtered_df)
    
    # Output the results
    output_results(complaint_counts, args.output)

if __name__ == "__main__":
    main()

