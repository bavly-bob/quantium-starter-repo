import csv
import os

def process_sales_data(input_dir, output_file):
    """
    Reads CSV files from input_dir, filters for 'pink morsel',
    calculates sales (price * quantity), and writes to output_file.
    """
    
    header = ["sales", "date", "region"]
    output_rows = []

    # Iterate through all files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".csv"):
            filepath = os.path.join(input_dir, filename)
            
            with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row in reader:
                    product = row['product']
                    
                    # Filter for "pink morsel"
                    if product == "pink morsel":
                        price_str = row['price']
                        quantity_str = row['quantity']
                        date = row['date']
                        region = row['region']
                        
                        # Remove '$' from price and convert to float
                        price = float(price_str.replace('$', ''))
                        quantity = int(quantity_str)
                        
                        # Calculate sales
                        sales = price * quantity
                        
                        output_rows.append([sales, date, region])

    # Write to output file
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(header)
        writer.writerows(output_rows)

    print(f"Successfully processed data into {output_file}")

if __name__ == "__main__":
    # Define input directory (assumed to be 'data' relative to script)
    input_directory = os.path.join(os.path.dirname(__file__), 'data')
    output_filename = "formatted_output.csv"
    
    # Run the processing function
    process_sales_data(input_directory, output_filename)
