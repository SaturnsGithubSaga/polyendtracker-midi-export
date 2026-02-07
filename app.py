import streamlit as st
import os
import zipfile
import shutil
import tempfile
import sys
from io import BytesIO
import subprocess

st.title("🎹 Polyend Tracker to MIDI Converter")
st.write("Upload a **ZIP file** of your Polyend Project folder (containing the .mt file and patterns folder).")

uploaded_file = st.file_uploader("Choose your project ZIP", type="zip")

if uploaded_file is not None:
    # Create a temporary directory to process the files
    with tempfile.TemporaryDirectory() as temp_dir:
        # 1. Extract the ZIP file
        project_path = os.path.join(temp_dir, "project")
        os.makedirs(project_path, exist_ok=True)
        
        with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
            zip_ref.extractall(project_path)
        
        # Users might zip the folder 'MyProject' or just the contents.
        # We walk through the extracted files to find the .mt file to locate the root.
        root_dir = project_path
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file.endswith(".mt"):
                    root_dir = root
                    break
        
        st.write(f"Project found in: `{root_dir}`")
        
        # 2. Run the conversion
        # We invoke the python script as a subprocess on the extracted directory.
        cmd = [sys.executable, "polytracker2midi.py", root_dir]
        
        with st.spinner('Converting to MIDI...'):
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
            
        if result.returncode != 0:
            st.error("Something went wrong during conversion!")
            st.code(result.stderr)
        else:
            st.success("Conversion successful! 🎉")
            # st.code(result.stdout) # Uncomment for debug info
            
            # 3. Package everything for download
            # We look for .mid files in the directory
            output_zip_buffer = BytesIO()
            with zipfile.ZipFile(output_zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
                for root, dirs, files in os.walk(root_dir):
                    for file in files:
                        if file.endswith(".mid"):
                            # Make the path relative so the zip structure is clean
                            abs_path = os.path.join(root, file)
                            rel_path = os.path.relpath(abs_path, root_dir)
                            zf.write(abs_path, rel_path)
            
            st.download_button(
                label="⬇️ Download MIDI Files (ZIP)",
                data=output_zip_buffer.getvalue(),
                file_name="converted_midi.zip",
                mime="application/zip"
            )
