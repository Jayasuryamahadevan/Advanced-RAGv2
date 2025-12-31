# Base Image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set Environment Variables
# Default to host.docker.internal for Mac/Windows to access host Ollama
ENV OLLAMA_BASE_URL="http://host.docker.internal:11434"
ENV PYTHONPATH=/app

# Default command
ENTRYPOINT ["python", "agentic_interactive.py"]
CMD ["sales.csv"]
