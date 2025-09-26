# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables to prevent Python from writing pyc files and to buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (build tools, SQLite, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libsqlite3-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port Hypercorn will listen on
EXPOSE 8000

# Command to run the app with Hypercorn
# Adjust the module path if your app is in a package (e.g., "myapp.app:app")
CMD ["hypercorn", "app:app", "--bind", "0.0.0.0:8000", "--worker-class", "asyncio"]
