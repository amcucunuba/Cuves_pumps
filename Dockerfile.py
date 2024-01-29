# Use the official Python image as the base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /esp_app

# Copy the application files into the working directory
COPY . /app_esp.py 

# Install the application dependencies
RUN pip install -r requirements.txt

# Expose the port on which the app will run
EXPOSE 8000
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