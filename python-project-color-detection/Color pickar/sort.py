import csv
import os

# Define function to normalize color names
def normalize_color_name(color_name):
    return color_name.strip().lower()

# Open input CSV file and read data into a list
input_filename = 'named_colors_output.csv'
if not os.path.isfile(input_filename):
    print(f"Input file '{input_filename}' does not exist")
    exit(1)

# Open output CSV file for writing
output_filename = 'output.csv'
try:
    output_file = open(output_filename, 'w', newline='')
    fieldnames = ['Color Name', 'Color Name (Title Case)', 'Hex Code', 'Red', 'Green', 'Blue']
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    writer.writeheader()
except Exception as e:
    print(f"Error opening output file '{output_filename}': {e}")
    exit(1)

# Sort and de-duplicate data row by row
previous_color_name = None
with open(input_filename, newline='') as input_file:
    reader = csv.DictReader(input_file)
    for row in sorted(reader, key=lambda x: (int(x['Red']), int(x['Green']), int(x['Blue']))):
        current_color_name = normalize_color_name(row['Color Name'])
        if current_color_name != previous_color_name:
            writer.writerow(row)
            previous_color_name = current_color_name

# Close output CSV file
try:
    output_file.close()
except Exception as e:
    print(f"Error closing output file '{output_filename}': {e}")
    exit(1)

print(f"Successfully wrote de-duplicated data to '{output_filename}'")
