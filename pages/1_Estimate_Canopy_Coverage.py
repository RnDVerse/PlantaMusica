import streamlit as st
import numpy as np
import cv2
from PIL import Image
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(layout="wide", page_title="Count Canopy Coverage", page_icon="📊")

# Page title
st.markdown("# Estimate Canopy Coverage of a Plant")
st.sidebar.header("Estimate Canopy Coverage through pixels and then calibrate to cm^2")

st.write(
    """Upload an image of a series of image of plants with green colored canopy. The canopy coverage will be calculated based on existing pixel scaling. 
      Function for custom pixels adjustment is being worked on. You can improve the accuracy by first removing the background image through the plantamusica tab.  """
)
# Define maximum file size
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Helper function to convert and save image
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

# Image processing function
def process_image(upload):
    image = Image.open(upload)
    col1, col2 = st.columns(2)
    col1.write("Original Image :camera:")
    col1.image(image)

    # Convert image to array and then to HSV
    image_array = np.array(image.convert('RGB'))  # Ensure image is in RGB
    hsv_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2HSV)

    # Define the range for green color in HSV and create a mask
    lower_green = np.array([35, 50, 50])
    upper_green = np.array([85, 255, 255])
    mask = cv2.inRange(hsv_image, lower_green, upper_green)

    # Convert mask back to an image for display
    mask_image = Image.fromarray(mask)
    processed_image = mask_image

    col2.write("Processed Image :wrench:")
    col2.image(processed_image, use_column_width=True)
    return processed_image, image_array  # Return both processed mask and original RGB array

# Function to calculate Canopy Coverage in pixels
def get_area_in_pixels(mask):
    # Calculate the Canopy Coverage pixels directly from the mask
    green_area_pixels = np.sum(mask == 255)
    return green_area_pixels


# Uploading and handling multiple images
uploaded_files = st.sidebar.file_uploader("Upload images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

# Initialize lists to store results for plotting and displaying
canopy_areas = []
image_names = []

if uploaded_files:
    for uploaded_file in uploaded_files:
        if uploaded_file.size > MAX_FILE_SIZE:
            st.error(f"The file {uploaded_file.name} is too large. Please upload an image smaller than 5MB.")
        else:
            # Process each image and display
            processed_image, original_image = process_image(uploaded_file)
            pixel_area = get_area_in_pixels(np.array(processed_image))
            scaling_factor = 4096  # obtained from calibration
            green_area_cm2 = pixel_area / scaling_factor
            canopy_areas.append(green_area_cm2)
            image_names.append(uploaded_file.name)

            # Display the green area for each image
            st.write(f"The Canopy Coverage for {uploaded_file.name} is {green_area_cm2} cm²")
else:
    st.warning("Please upload an image or images to continue.")


# Calculate and display Canopy Coverage if an image has been processed
if 'original_image' in locals():
    pixel_area = get_area_in_pixels(np.array(processed_image))
    scaling_factor = 4096  # obtained from calibration
    st.write(f"The Canopy Coverage is {pixel_area / scaling_factor} cm²")

# If there are results, display them in a table and plot
if canopy_areas:

    
    # Create a DataFrame for displaying results in a table
    results_df = pd.DataFrame({
        "Image Name": image_names,
        "Canopy Coverage (cm²)": canopy_areas
    })
    
    # Display the DataFrame as a table
    st.write("### Canopy Coverage Results", results_df)
    
    # Plot the results
    fig, ax = plt.subplots()
    ax.bar(image_names, canopy_areas, color='green')
    ax.set_xlabel('Image Name')
    ax.set_ylabel('Canopy Coverage (cm²)')
    ax.set_title('Canopy Coverage of Plants')
    ax.set_xticklabels(image_names, rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)


# Button to rerun the app (triggers a rerun of the script)
st.button("Re-run")