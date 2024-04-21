import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO
import base64

st.set_page_config(layout="wide", page_title="Planta Musica [alpha-version]")

st.write("## Analyze Plant & Music")
st.write(""":tree: Try uploading an image to preprocess, and obtain your picked color (using HSV range for now) color-picker will be added later. 
         Full quality processed images can be downloaded from the side bar. This code is open source and available [here](https://github.com/RnDVerse/PlantaMusica) on GitHub. Share with others if you find this useful :heart: learn more about the project [here](https://www.researchhub.com/hubs/lettuce-growth-and-music-data). 
         This is a mere test deployment, several features are under development and will be updated soon (hopefully in a week or so). Have Fun!
        """
)
st.sidebar.write("## Upload and download :gear:")

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Download the fixed image
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im


def fix_image(upload):
    image = Image.open(upload)
    col1.write("Original Image :camera:")
    col1.image(image)

    fixed = remove(image)
    col2.write("Fixed Image :wrench:")
    col2.image(fixed)
    st.sidebar.markdown("\n")
    st.sidebar.download_button("Download fixed image", convert_image(fixed), "fixed.png", "image/png")




### MAIN APP Start here 

col1, col2 = st.columns(2)
my_upload = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if my_upload is not None:
    if my_upload.size > MAX_FILE_SIZE:
        st.error("The uploaded file is too large. Please upload an image smaller than 5MB.")
    else:
        fix_image(upload=my_upload)
else:
    fix_image("./images/plant.jpg")
