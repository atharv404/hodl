FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    sqlite3 \
    gcc \
    g++ \
    make \
    libv8-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create necessary directories
RUN mkdir -p /app/db /app/logs

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt || \
    pip install --no-cache-dir flask sqlalchemy werkzeug pycryptodome json5 mmh3 twisted coloredlogs dpath

# Copy application code
COPY . .

# Install the package
RUN python setup.py develop

# Expose port
EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8001/status || exit 1

# Run the application
CMD ["python", "-m", "hodl.daemon"]
