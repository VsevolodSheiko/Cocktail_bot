# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the bot files to the working directory
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Install dependencies
RUN pip install -r requirements.txt
RUN apt-get update \
    && apt-get install -y sqlite3

# Expose the port that your bot will run on
EXPOSE 3001

# Command to run your bot
CMD ["python", "main.py"]
