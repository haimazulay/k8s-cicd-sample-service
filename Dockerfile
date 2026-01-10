# Stage 1: Builder
FROM python:3.12-slim AS builder

WORKDIR /app

# Install dependencies into a temporary directory
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim

WORKDIR /app

# Create a non-root user with explicit UID
RUN addgroup --system --gid 10001 appgroup && \
    adduser --system --uid 10001 --gid 10001 --no-create-home appuser

# Copy installed dependencies from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY app.py .

# Switch to non-root user
USER appuser

# Expose the application port
EXPOSE 8080

# Run with Gunicorn (production server)
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8080", "--access-logfile", "-", "app:app"]
