# Use the official Python image as base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the Python script and credentials file into the container
COPY main.py credentials.json /app/

# Install the necessary Python packages
RUN pip install google-api-python-client

# Run the Python script
CMD ["python", "main.py"]