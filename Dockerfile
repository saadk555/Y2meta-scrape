FROM python:3.9

# Install system dependencies for Chromium, Xvfb, and WebDriverManager
RUN apt-get update && apt-get install -y chromium xvfb 
RUN wget https://dl.google.com/linux/linux_signing_key.pub \
    && apt-key add linux_signing_key.pub \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \ 
    && apt-get update \
    && apt-get install -y google-chrome-stable

# Create a working directory within the image
WORKDIR /app

# Copy your project's requirements file
COPY requirements.txt ./

# Install Python dependencies (including WebDriverManager)
RUN pip install -r requirements.txt

# Copy all your Selenium and API project files
COPY . ./


# Expose the port on which Flask runs
EXPOSE 5000 

# Command to start your Flask API when the container runs
# ... other parts ...

CMD Xvfb :99 -screen 0 1024x768x24 & export DISPLAY=:99 && python app.py > output.log

