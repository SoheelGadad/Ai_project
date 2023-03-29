import cv2
import numpy as np
import pandas as pd
import argparse
import tkinter as tk
from tkinter import filedialog

# Creating argument parser to take image path from command line
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=False, help="Image Path")
args = vars(ap.parse_args())

root = tk.Tk()
root.withdraw()

# Open file dialog to select an image
file_path = filedialog.askopenfilename()

if file_path:
    img_path = file_path
elif args["image"]:
    img_path = args["image"]
else:
    print("Please provide an image path")

# Reading the image with opencv
img = cv2.imread(img_path)

# Declaring global variables (are used later on)
clicked = False
r = g = b = xpos = ypos = 0

# Reading csv file with pandas and giving names to each column
csv = pd.read_csv('named_colors_output.csv')

# Function to calculate minimum distance from all colors and get the most matching color
def getColorName(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if(d <= minimum):
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

# Function to get x,y coordinates of mouse click
def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        global b, g, r
        b, g, r = img[y, x]
        color_scanner = np.zeros((300, 300, 3), np.uint8)
        color_scanner[:, :] = (b, g, r)
        cv2.putText(color_scanner, "B: {} G: {} R: {}".format(b, g, r), (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.imshow('color_scanner', color_scanner)

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)


while True:
    # Set maximum size of the image
    max_size = 800 

    # Calculate the scale percent based on the maximum size and the image's original size
    scale_percent = min(max_size / img.shape[1], max_size / img.shape[0]) * 100

    # Calculate the new dimensions of the scaled image
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)

    # Resize the image
    scaled_img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    # Display the scaled image
    cv2.imshow("image", scaled_img)

    # Update the color rectangle and text when the user clicks on the image
    # Update the color rectangle and text when the user clicks on the image
    text = ""
    if clicked:
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)
        text = getColorName(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

    # Set font properties
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    thickness = 2

    # Get the size of the text
    text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)

    # Position the text within the color rectangle
    text_x = 50
    text_y = 50
    if text_x + text_size[0] >= img.shape[1]:
        text_x = img.shape[1] - text_size[0] - 10
    if text_y + text_size[1] >= img.shape[0]:
        text_y = img.shape[0] - text_size[1] - 10

    # Set the font color based on the brightness of the color
    font_color = (0, 0, 0) if r + g + b >= 600 else (255, 255, 255)

    # Add the text to the image
    cv2.putText(img, text, (text_x, text_y), font, font_scale, font_color, thickness, cv2.LINE_AA)

# Wait for the space bar to be pressed to scan colors
    if cv2.waitKey(20) & 0xFF == 32:
        cv2.destroyAllWindows()

# Wait for the space bar to be pressed to scan colors
    if cv2.waitKey(20) & 0xFF == 32:  
     cv2.destroyAllWindows()

    # Get the height and width of the image
    h, w, _ = img.shape  

    # Create an empty image for the color scan result
    color_scan = np.zeros([h, w, 3], dtype=np.uint8)  

    # Fill the color scan image with selected pixels if they exist within the image
    if ypos - 10 >= 0 and ypos + 10 < h and xpos - 10 >= 0 and xpos + 10 < w:
        color_scan[:, :, :] = img[ypos - 10:ypos + 10, xpos - 10:xpos + 10, :]

       # Create a named window for the color scan result
    cv2.namedWindow("Color Scan Result", cv2.WINDOW_NORMAL)

    # Resize the named window to a specific size
    cv2.resizeWindow("Color Scan Result", 400, 400)

    # Display the color scan result
    cv2.imshow("Color Scan Result", color_scan)
# Adding Zoom functionality
    key = cv2.waitKey(1)
    if key == ord('+'): # Zoom in
        img = cv2.resize(img, None, fx=1.1, fy=1.1, interpolation=cv2.INTER_LINEAR)
    elif key == ord('-'): # Zoom out
        img = cv2.resize(img, None, fx=0.9, fy=0.9, interpolation=cv2.INTER_LINEAR)

#Break the loop when user hits 'esc' key
    if key == 27: # 'esc' key
         break
    elif cv2.getWindowProperty('image', cv2.WND_PROP_VISIBLE) < 1: # window closed by user
        break
cv2.destroyAllWindows()