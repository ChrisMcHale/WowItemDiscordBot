import os

import cv2
import numpy as np


def crop_image(image_to_crop):
    # Load the image
    image = cv2.imread(image_to_crop)
    # Convert to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Define the range for gold color in HSV
    # You may need to adjust these values based on your image
    lower_gold = np.array([15, 100, 100])  # Lower bound of gold color
    upper_gold = np.array([30, 255, 255])  # Upper bound of gold color
    # Create a mask for the gold color
    mask = cv2.inRange(hsv_image, lower_gold, upper_gold)
    # Find contours of the gold box
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Ensure at least one contour is found
    if len(contours) > 0:
        # Find the largest contour by area
        largest_contour = max(contours, key=cv2.contourArea)

        # Get the bounding box for the largest contour
        x, y, w, h = cv2.boundingRect(largest_contour)

        # Crop the image to the bounding box
        cropped_image = image[y:y + h, x:x + w]

        # Save or display the cropped image
        base_filename = os.path.splitext(os.path.basename(image_to_crop))[0]
        output_image_path = f"{base_filename}_cropped.png"
        cv2.imwrite(output_image_path, cropped_image)
        print(f"Cropped image saved as {output_image_path}")

    else:
        print("No gold box found!")
