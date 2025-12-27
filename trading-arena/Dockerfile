# Trading Arena API - Production Dockerfile
# Multi-stage build for smaller image

FROM python:3.12-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.12-slim

WORKDIR /app

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash arena

# Copy installed packages from builder to arena user's home
COPY --from=builder /root/.local /home/arena/.local
RUN chown -R arena:arena /home/arena/.local

# Set path for arena user
ENV PATH=/home/arena/.local/bin:$PATH

# Copy application code and set ownership
COPY --chown=arena:arena api ./api

USER arena

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8080/v1/health')" || exit 1

# Run with uvicorn
CMD ["python", "-m", "uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8080"]
