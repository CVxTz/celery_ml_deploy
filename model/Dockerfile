# Use the official Python 3.11 image from the Docker Hub
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu

# Create a non-root user and set up permissions
RUN useradd -m myuser

# Copy all .py files into the container
COPY *.py .

# Change ownership of the /app directory to the new user
RUN chown -R myuser:myuser /app

# Switch to the non-root user
USER myuser

RUN python model.py

# Command to run on container start
CMD ["python", "worker.py"]