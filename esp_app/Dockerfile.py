# Use the official Python image as the base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the application files into the working directory
COPY . /requirements.txt .

# Install the application dependencies
RUN pip install -r requirements.txt

# Define the entry point for the container
CMD ["python", "app_esp.py", "runserver", "0.0.0.0:8000"]

FROM --platform=$BUILDPLATFORM node:18-alpine AS app-base
WORKDIR /esp_app
COPY esp_app/app_esp.py 
COPY esp_app/assets ./assets


# Run tests to validate app
FROM esp_app-base AS test
RUN app_esp.py  install
RUN app_esp.py  test