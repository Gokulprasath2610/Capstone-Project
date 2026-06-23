# Multi-stage build for Agentic AI Loan Approval System

# Stage 1: Base Python environment
FROM python:3.11-slim as base

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: FastAPI service
FROM base as fastapi-service

WORKDIR /app

COPY config.py .
COPY orchestration_engine.py .
COPY fastapi_service.py .
COPY database.py .
COPY fastmcp_servers.py .
COPY mcp_servers.py .

ENV PYTHONUNBUFFERED=1
ENV FASTAPI_HOST=0.0.0.0
ENV FASTAPI_PORT=8000

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "fastapi_service.py"]


# Stage 3: Streamlit UI
FROM base as streamlit-ui

WORKDIR /app

COPY config.py .
COPY orchestration_engine.py .
COPY streamlit_app.py .
COPY database.py .
COPY fastmcp_servers.py .
COPY mcp_servers.py .

ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_PORT=8501
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "streamlit_app.py"]


# Stage 4: Complete system (for development)
FROM base as complete

WORKDIR /app

COPY . .

ENV PYTHONUNBUFFERED=1

# By default, this stage doesn't expose anything
# Use docker-compose to run individual services

CMD ["bash"]
