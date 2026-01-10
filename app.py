import logging
import sys
from flask import Flask, jsonify
from pythonjsonlogger import jsonlogger

# Configure structured logging
logger = logging.getLogger()
logHandler = logging.StreamHandler(sys.stdout)
formatter = jsonlogger.JsonFormatter(
    "%(asctime)s %(levelname)s %(name)s %(message)s"
)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

app = Flask(__name__)

@app.route("/")
def index():
    logger.info("Handling request to /")
    return "Hello from k8s-cicd-sample-service\n"

@app.get("/healthz")
def healthz():
    """Liveness probe endpoint"""
    logger.debug("Liveness probe checked")
    return "ok\n", 200

@app.get("/ready")
def ready():
    """Readiness probe endpoint"""
    logger.debug("Readiness probe checked")
    return "ready\n", 200

if __name__ == "__main__":
    # This block is for local development only.
    # In production, use gunicorn: gunicorn -w 2 -b 0.0.0.0:8080 app:app
    logger.info("Starting application in development mode")
    app.run(host="0.0.0.0", port=8080)
