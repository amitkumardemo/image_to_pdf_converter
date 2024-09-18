import streamlit as st
from PIL import Image
from fpdf import FPDF
import io
import tempfile

# Set page configuration
st.set_page_config(page_title="Image to PDF Converter", layout="wide")

# Logo
st.image("jb.png", width=250)  # Replace with your logo URL

# Navbar
st.markdown("""
<div class="navbar">
  <a href="#Home">Home</a>
  <a href="#About">About</a>
  <a href="https://techiehelpt.netlify.app/">Back To Website</a>
</div>
""", unsafe_allow_html=True)

# Add navigation to different sections
menu = ["Home", "About"]
choice = st.sidebar.selectbox("Navigate", menu)

if choice == "Home":
    # Home Page
    st.title("Image to PDF Converter")
    st.write("Upload images (up to 100+) to convert them into a PDF document.")

    # File uploader for image input
    uploaded_files = st.file_uploader("Choose images...", type=["jpg", "png", "jpeg"], accept_multiple_files=True, label_visibility="visible")

    if uploaded_files:
        if len(uploaded_files) > 100:
            st.warning("You have uploaded more than 100 images. Please ensure this does not affect performance.")

        # Create a PDF document
        pdf = FPDF()
        pdf.set_auto_page_break(0)

        for uploaded_file in uploaded_files:
            # Open the uploaded image
            image = Image.open(uploaded_file)

            # Convert image to RGB if it is RGBA or other modes
            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")

            # Save the image to a temporary file
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
                image.save(temp_file, format='JPEG')
                temp_file_path = temp_file.name

            # Add image to PDF
            pdf.add_page()
            pdf.image(temp_file_path, x=0, y=0, w=210, h=297)  # A4 size dimensions

        # Save the PDF to a temporary file
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_pdf_file:
            pdf.output(temp_pdf_file.name)
            temp_pdf_path = temp_pdf_file.name

        # Read the PDF into a BytesIO object
        with open(temp_pdf_path, "rb") as f:
            pdf_buffer = io.BytesIO(f.read())

        # Download button for the PDF document
        st.download_button(
            label="📥 Download PDF",
            data=pdf_buffer,
            file_name="images.pdf",
            mime="application/pdf"
        )

elif choice == "About":
    # About Page
    st.title("About Image to PDF Converter")
    st.write("""
    This tool allows you to upload images and convert them into a PDF document.

    **Features**:
    - Upload multiple images (up to 100+).
    - Images are sequentially arranged in the generated PDF.
    - Download the resulting PDF document.

    **Technology Stack**:
    - Streamlit (for building the web app)
    - Pillow (for image handling)
    - FPDF (for creating PDF documents)
    """)

# Footer
st.markdown("""
<div class="footer">
    <p>© 2024 Image to PDF Converter | TechieHelp</p>
    <a href="https://www.linkedin.com/in/techiehelp" style="color:white; margin-right: 10px;">LinkedIn</a>
    <a href="https://www.twitter.com/techiehelp" style="color:white; margin-right: 10px;">Twitter</a>
    <a href="https://www.instagram.com/techiehelp2" style="color:white;">Instagram</a>
</div>
""", unsafe_allow_html=True)
