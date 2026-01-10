# k8s-cicd-sample-service

A live example service demonstrating the usage of the [Kubernetes CI/CD Templates](https://github.com/haimazulay/github-k8s-cicd-templates).

This repository serves as a reference implementation for onboarding applications to the centralized CI/CD pipeline.

## Repository Contents

*   **Application**: A Python Flask service (`app.py`) exposing `/healthz` and `/ready` endpoints.
*   **Dockerfile**: Configuration to build the application container.
*   **Helm Chart**: Located in `helm/` for Kubernetes deployment.
*   **CI/CD Workflows**: Minimal "caller" workflows in `.github/workflows/` that inherit logic from the templates repository.

## End-to-End CI/CD Flow

The pipeline is divided into three levels, each triggered by specific Git events:

### 1. Level 1: Pull Request (Validation)
**File:** `.github/workflows/l1-pr.yml`

*   **Trigger**: Open a Pull Request targeting `main`.
*   **What it does**:
    *   Checkouts code.
    *   Builds the Docker image (test build, no push).
    *   Lints the Helm chart (`helm lint`).
    *   Packages the Helm chart.
*   **Goal**: Ensure the code is buildable and the chart is valid before merging.

### 2. Level 2: Push (Build & Publish)
**File:** `.github/workflows/l2-push.yml`

*   **Trigger**: Push to branches (e.g., `feature/**`, `develop`, `main`).
*   **What it does**:
    *   Runs application validation (tests/lints).
    *   Builds the Docker image.
    *   Pushes the image to the container registry (e.g., GHCR or Docker Hub) if secrets are configured.
*   **Goal**: Create and publish immutable artifacts for every commit.

### 3. Level 3: Merge (Deploy & Verify)
**File:** `.github/workflows/l3-merge.yml`

*   **Trigger**: Merge (push) to `main`.
*   **What it does**:
    *   Creates an ephemeral Kubernetes cluster using `kind`.
    *   Deploys the application using the local Helm chart and the built image.
    *   Wait for the rollout to complete.
    *   Verifies the application availability.
*   **Goal**: Simulate a real deployment and verify the service runs correctly in a Kubernetes environment.

## Application Endpoints

The service listens on port **8080**.

*   `GET /`: Returns a welcome message.
*   `GET /healthz`: Liveness probe (Returns 200 OK).
*   `GET /ready`: Readiness probe (Returns 200 OK).

## How to Run Locally

```bash
# Install dependencies
pip install flask

# Run application
python app.py
```

## How to Onboard Your Service

To use this CI/CD setup in your own repository:
1. Copy the `.github/workflows/*.yml` files.
2. Copy the `helm/` directory (or use your own chart).
3. Ensure your `Dockerfile` exists.
4. Update `inputs` in the workflow files (e.g., `image_name`, `chart_path`) if necessary.