import pandas as pd
import os
import sys

def create_dataset(company, date, total_amount, tax_amount, gst):
    # Create the dataset
    data = {
        "Company": [company],  # Wrap in lists
        "Date": [date],
        "Total Amount": [total_amount],
        "Tax Amount": [tax_amount],
        "GST": [gst]
    }

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Define the CSV file path
    csv_file_path = 'daily_expenditure.csv'

    # Check if the file already exists
    if os.path.isfile(csv_file_path):
        # Append data to the existing CSV without writing the header
        df.to_csv(csv_file_path, mode='a', header=False, index=False)
    else:
        # Write the data with the header for the first time
        df.to_csv(csv_file_path, mode='w', header=True, index=False)

    print(f"Data saved to {csv_file_path}")
    return df

# Example usage passing command-line arguments
create_dataset(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
