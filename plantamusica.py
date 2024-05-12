import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO
import zipfile

st.set_page_config(layout="wide", page_title="Planta Musica [alpha-version]")

st.write("## Analyze Plant Canopy Coverage and Environment Conditions")
st.write("""
         Try uploading images to preprocess, and obtain your picked color (using ad-hoc HSV range for now) color-picker will be added later. 
         Full quality processed images can be downloaded from the side bar. 
         This code is open source and available [here](https://github.com/RnDVerse/PlantaMusica) on GitHub. 
         Share with others if you find this useful :heart: learn more about the project [here](https://www.researchhub.com/hubs/lettuce-growth-and-music-data). 
         This mini-app is in test deployment mode, several features are under development and will be updated soon (hopefully in a week or so). Have Fun!
        """)
st.write("Don't forget to check out the other sections:")
st.write("1. Estimate Canopy Coverage")
st.write("2. Extract Environment Condition")
st.write("3. Correlation and Plotting")
st.write("4. Music Analysis")

st.sidebar.write("## Upload and download :gear:")

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB limit per file

# Convert image for download
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

# Process and fix image
def fix_images(uploads):
    zipped_file = BytesIO()
    with zipfile.ZipFile(zipped_file, 'w') as zfile:
        for idx, upload in enumerate(uploads):
            image = Image.open(upload)
            col1, col2 = st.columns(2)
            col1.write(f"Original Image {idx + 1} :camera:")
            col1.image(image)

            fixed = remove(image)
            col2.write(f"Fixed Image {idx + 1} :wrench:")
            col2.image(fixed)

            # Save fixed image to ZIP
            img_byte_arr = BytesIO()
            fixed.save(img_byte_arr, format='PNG')
            zfile.writestr(f"fixed_image_{idx + 1}.png", img_byte_arr.getvalue())

    zipped_file.seek(0)
    return zipped_file

# Main app logic
uploads = st.sidebar.file_uploader("Upload images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
if uploads:
    if any(upload.size > MAX_FILE_SIZE for upload in uploads):
        st.error("One or more files are too large. Please upload images smaller than 5MB each.")
    else:
        zipped_file = fix_images(uploads)
        st.sidebar.download_button("Download All Fixed Images as ZIP", zipped_file, "fixed_images.zip", "application/zip")
