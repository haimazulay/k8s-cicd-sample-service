FROM python:3.12-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir flask

# Copy application code
COPY app.py .

# Expose the application port (for documentation only)
EXPOSE 8080

# Run the Flask app
CMD ["python", "app.py"]
