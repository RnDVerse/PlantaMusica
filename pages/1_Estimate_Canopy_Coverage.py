import streamlit as st
import numpy as np
import cv2
from PIL import Image
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="Planta Musica [alpha-version v0.2]")

st.write("## Analyze Plant Canopy Coverage and Environment Conditions")
st.write("""
         Try uploading images to preprocess, and obtain your picked color (using ad-hoc HSV range for now) color-picker will be added later. 
         Full quality processed images can be downloaded from the side bar. 
         This code is open source and available [here](https://github.com/RnDVerse/PlantaMusica) on GitHub. 
         Share with others if you find this useful :heart: learn more about the project [here](https://www.researchhub.com/hubs/lettuce-growth-and-music-data). 
         This mini-app is in test deployment mode, several features are under development and will be updated soon (hopefully in a week or so). Have Fun!
        """)
st.write("1. Estimate Canopy Coverage")
st.write("2. Data Analysis, Correlation, and Plotting")
st.write("3. Music Analysis")


st.sidebar.write("## Upload and download :gear:")

# Define maximum file size
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Helper function to convert and save image
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format=img.format)
    byte_im = buf.getvalue()
    return byte_im

# Image processing function
def process_image(image):
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

# Automatically analyze the default images at the beginning
default_images_paths = ["images/Day20.jpg", "images/Day22.jpg", "images/Day24.jpg","images/Day26.jpg","images/Day28.jpg"]
canopy_areas = []
image_names = []

for image_path in default_images_paths:
    image = Image.open(image_path)
    processed_image, original_image = process_image(image)
    pixel_area = get_area_in_pixels(np.array(processed_image))
    scaling_factor = 4096  # obtained from calibration
    green_area_cm2 = pixel_area / scaling_factor
    canopy_areas.append(green_area_cm2)
    image_names.append(image_path.split('/')[-1])

    # Display the green area for each default image
    st.write(f"The Canopy Coverage for {image_path.split('/')[-1]} is {green_area_cm2} cm²")


# Uploading and handling multiple images
uploaded_files = st.sidebar.file_uploader("Upload images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        if uploaded_file.size > MAX_FILE_SIZE:
            st.error(f"The file {uploaded_file.name} is too large. Please upload an image smaller than 5MB.")
        else:
            # Process each image and display
            image = Image.open(uploaded_file)
            processed_image, original_image = process_image(image)
            pixel_area = get_area_in_pixels(np.array(processed_image))
            scaling_factor = 4096  # obtained from calibration
            green_area_cm2 = pixel_area / scaling_factor
            canopy_areas.append(green_area_cm2)
            image_names.append(uploaded_file.name)

            # Display the green area for each image
            st.write(f"The Canopy Coverage for {uploaded_file.name} is {green_area_cm2} cm²")
else:
    st.warning("Please upload an image or images to continue.")

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