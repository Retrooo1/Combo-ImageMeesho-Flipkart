import streamlit as st
import os
import zipfile
import base64
from jtest2 import run

input__folder = "receivedPath"
output__folder = "savedPath"

def save_uploaded_file(uploaded_file):
    with open(os.path.join(input__folder, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

with st.form("my_form"):
    uploaded_files = st.file_uploader("Upload your images", accept_multiple_files=True)
    margin = st.slider("Margin (in pixels)", min_value=0, max_value=100, step=1)
    color = st.slider("Color (0-255)", min_value=0, max_value=255, step=1)
    height = st.number_input("Height (in pixels)", min_value=100, max_value=1000, value=500, step=10)
    width = st.number_input("Width (in pixels)", min_value=100, max_value=1000, value=500, step=10)
    size = (height, width)

    submitted = st.form_submit_button("Submit")

if submitted and uploaded_files:
    if os.path.exists(input__folder) == False:
        os.mkdir(input__folder)
    for uploaded_file in uploaded_files:
        save_uploaded_file(uploaded_file)

    run(margin, color, size, input__folder, output__folder)

    max_size = 150 * 1024 * 1024  # 200 MB
    zip_count = 1
    zip_size = 0
    zipf = zipfile.ZipFile(os.path.join(output__folder, f"images_{zip_count}.zip"), 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(output__folder):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            if zip_size + file_size > max_size:
                zipf.close()
                zip_count += 1
                zip_size = 0
                zipf = zipfile.ZipFile(os.path.join(output__folder, f"images_{zip_count}.zip"), 'w', zipfile.ZIP_DEFLATED)
            zip_size += file_size
            zipf.write(file_path)
            print("Made file",file_path)
    zipf.close()
    print("Made all zips")

    # Download buttons for all zips
    print("A1")
    zip_files = [f for f in os.listdir(output__folder) if f.endswith(".zip")]
    print("A2")
    for zip_file in zip_files:
        print("A3"+str(zip_file))
        zip_path = os.path.join(output__folder, zip_file)
        with open(zip_path, "rb") as f:
            bytes_read = f.read()
            b64 = base64.b64encode(bytes_read).decode()
            size = os.path.getsize(zip_path)
            href = f'<a href="data:file/zip;base64,{b64}" download="{zip_file}">Download {zip_file} ({size} bytes)</a>'
            st.markdown(href, unsafe_allow_html=True)
