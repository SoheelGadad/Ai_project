
import csv
import os
from tkinter import filedialog
from tkinter import Tk
from PIL import Image
from webcolors import rgb_to_name, rgb_to_hex
from tqdm import tqdm

# Create a Tkinter root window (hidden) to allow file dialog to be displayed
root = Tk()
root.withdraw()

# Ask the user to select an image file using a file dialog
image_file = filedialog.askopenfilename(title='Select Image File', filetypes=[('Image Files', '*.jpg;*.jpeg;*.png;*.gif')])

# Open the image file
im = Image.open(image_file)

# Create a dictionary to store the named colors found in the image
named_colors = {}

# Iterate through each pixel in the image and convert its RGB color to a named color (if possible)
for pixel in tqdm(im.getdata(), desc='Processing Image'):
    try:
        color_name = rgb_to_name(pixel)
        hex_code = rgb_to_hex(pixel)
        named_colors[color_name] = (hex_code, *pixel)
    except ValueError:
        pass

# Save the named colors, their RGB values, and hex codes to a CSV file
csv_file = 'named_colors.csv'
if os.path.exists(csv_file):
    with open(csv_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        existing_rows = list(reader)
else:
    existing_rows = []

# Check if the color is already in the CSV file
def color_exists(color_name, hex_code, r, g, b):
    for row in existing_rows:
        if row[0] == color_name and row[2] == hex_code and row[3] == str(r) and row[4] == str(g) and row[5] == str(b):
            return True
    return False

# Append the named colors, their RGB values, and hex codes to the CSV file
with open(csv_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    for row in existing_rows:
        writer.writerow(row)
    
    for color_name, color_data in tqdm(named_colors.items(), desc='Appending Data'):
        hex_code, r, g, b = color_data
        
        if not color_exists(color_name, hex_code, r, g, b):
            writer.writerow([color_name, f'"{color_name.title()}"', hex_code, r, g, b])

print('Named colors, RGB values, and hex codes saved to', csv_file)
