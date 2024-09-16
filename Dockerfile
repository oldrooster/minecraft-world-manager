# Step 1: Use official Python image to build the app
FROM python:3.10-slim AS builder

# Set working directory
WORKDIR /app

# Install necessary dependencies
RUN pip install flask
RUN pip install Jinja2
RUN pip install docker

# Copy the rest of the application code
COPY app.py .
COPY static/ static/
COPY templates/ templates/

# Expose Flask's default port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
