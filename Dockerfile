FROM python:3.9

# Install system dependencies for Chromium, Xvfb (virtual display), and your project
RUN apt-get update && apt-get install -y chromium xvfb 

# Create a working directory within the image
WORKDIR /app

# Copy your project's requirements file
COPY requirements.txt ./

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy all your Selenium and API project files
COPY . ./

# Expose the port on which Flask runs
EXPOSE 5000 

# Command to start your Flask API when the container runs
CMD ["python", "api.py"] 
