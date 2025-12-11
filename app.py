from flask import Flask

app = Flask(__name__)


@app.get("/")
def index():
    return "Hello from k8s-cicd-sample-service\n"


@app.get("/healthz")
def healthz():
    # Liveness probe endpoint
    return "ok\n", 200


@app.get("/ready")
def ready():
    # Readiness probe endpoint
    return "ready\n", 200


if __name__ == "__main__":
    # The port must match the containerPort in the Helm chart (default 8080)
    app.run(host="0.0.0.0", port=8080)
