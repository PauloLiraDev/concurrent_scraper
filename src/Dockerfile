FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    fonts-liberation \
    libnss3 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libxss1 \
    libasound2 \
    libgbm1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    curl -Lo "/tmp/chromedriver-linux64.zip" "https://storage.googleapis.com/chrome-for-testing-public/136.0.7103.49/linux64/chromedriver-linux64.zip" && \
    curl -Lo "/tmp/chrome-linux64.zip" "https://storage.googleapis.com/chrome-for-testing-public/136.0.7103.49/linux64/chrome-linux64.zip" && \
    unzip /tmp/chromedriver-linux64.zip -d /opt/ && \
    unzip /tmp/chrome-linux64.zip -d /opt/ && \
    cp -r /opt/chromedriver-linux64/* /opt/ && \
    cp -r /opt/chrome-linux64 /opt/chrome


# Define the working directory
WORKDIR /src

# Set environment variables
ENV PYTHONPATH=/
ENV PYTHONUNBUFFERED=1

# Copy the project files
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "automation.app:app", "--host", "0.0.0.0", "--port", "8000"]