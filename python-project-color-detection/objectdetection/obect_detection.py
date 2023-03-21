import cv2
import numpy as np
import pandas as pd

# Load the Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Load the input image
img = cv2.imread('input_image.jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

# Create an empty list to store the object colors
object_colors = []

# Loop through each detected face
for (x, y, w, h) in faces:
    # Extract the region of interest (ROI) containing the face
    roi = img[y:y+h, x:x+w]

    # Calculate the average color of the ROI
    avg_color = np.mean(roi, axis=(0, 1))

    # Convert the color from BGR to RGB
    avg_color_rgb = tuple(reversed(avg_color))

    # Append the color to the list of object colors
    object_colors.append(avg_color_rgb)

# Create a DataFrame to store the object colors
df = pd.DataFrame({'color': object_colors})

# Save the DataFrame to a CSV file
df.to_csv('object_colors.csv', index=False)
