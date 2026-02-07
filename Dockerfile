# Start with a slim Python version
FROM python:3.12-slim

# Set working directory in the container
WORKDIR /app

# Install system tools (git is required if setup.py uses it, otherwise optional but good practice)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the files (script, library patches, etc.)
COPY . .

# CRITICAL: Overwrite the standard MidiFile.py with OUR patched version.
# We locate where midiutil is installed and replace the file.

# This part has been changed because I want to publish the fixed code on Github, which Gemini at first didn't take into account. 
# RUN cp MidiFile.py $(python -c "import site; print(site.getsitepackages()[0])")/midiutil/MidiFile.py
# Copy the patch from the new folder
COPY patches/MidiFile.py /tmp/MidiFile.py
# Apply the patch
RUN cp /tmp/MidiFile.py $(python -c "import site; print(site.getsitepackages()[0])")/midiutil/MidiFile.py
# Expose the port for the web interface
EXPOSE 8501

# Command to run on container start
CMD sh -c "streamlit run app.py --server.port=${PORT:-8501} --server.address=0.0.0.0"
