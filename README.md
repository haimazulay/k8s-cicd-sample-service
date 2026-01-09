# GitHub Kubernetes CI/CD Templates

This repository provides reusable GitHub Actions workflows and a generic Helm chart
for onboarding application repositories into a Kubernetes-based CI/CD pipeline.

It is designed as a central **templates repo** that other services can copy from
(or be onboarded automatically by a dedicated onboarding workflow).

---

## Repository structure

```text
.github/
  workflows/
    l1-pr-build-and-package.yml   # Level 1 - PR validation
    l2-push-validate-and-build.yml# Level 2 - push build & optional registry push
    l3-merge-deploy.yml           # Level 3 - deploy to ephemeral kind cluster
helm/
  app-chart/
    Chart.yaml
    values.yaml
    templates/
      _helpers.tpl
      deployment.yaml
      service.yaml
      ingress.yaml
      serviceaccount.yaml
CI/CD Levels
Level 1 – PR Build & Helm Package
Workflow: .github/workflows/l1-pr-build-and-package.yml
Trigger: pull_request to main / develop

Main responsibilities:

Checkout the repository.

Build the Docker image (validation only, no push).

Install Helm.

Lint the Helm chart (helm lint).

Package the chart and upload it as a workflow artifact.

This level is focused on early feedback for developers before merging.

Level 2 – Push Validate & Build
Workflow: .github/workflows/l2-push-validate-and-build.yml
Trigger: push to main, develop, feature/**, hotfix/**

Main responsibilities:

Checkout the repository.

Run generic validation step (tests/linters placeholder).

Build the Docker image.

If Docker Hub credentials are configured:

Log in to Docker Hub.

Push the image with tags:

branch-<branch-name>

sha-<commit-sha>

This level ensures that every push can be built and, optionally, published to a registry.

Required secrets (optional but recommended):

DOCKERHUB_USERNAME

DOCKERHUB_TOKEN (Docker Hub access token)

Level 3 – Deploy on Merge to Main
Workflow: .github/workflows/l3-merge-deploy.yml
Trigger: push to main

Main responsibilities:

Checkout the repository.

Build the Docker image locally on the GitHub runner.

Create an ephemeral Kubernetes cluster using kind.

Load the locally built image into the kind cluster.

Install Helm.

Deploy (or upgrade) the Helm release using:

helm upgrade --install

Overriding:

fullnameOverride

image.repository

image.tag

Wait for the rollout to complete (kubectl rollout status).

On failure, print detailed debug information:

Pods

kubectl describe

Container logs

This level demonstrates a full CI/CD flow without requiring a long-lived external cluster.

Helm chart – helm/app-chart
The app-chart is a generic application Helm chart with:

Deployment with:

Configurable image repository/tag.

Probes:

GET /healthz for liveness.

GET /ready for readiness.

Configurable replicas, resources, node selectors, tolerations, affinity.

Service (ClusterIP by default).

Ingress (optional, disabled by default).

ServiceAccount (auto-created by default).

It assumes the application container:

Listens on port 8080.

Exposes:

GET /healthz

GET /ready

How to use these templates
1. Manual onboarding
For any application repository:

Copy the following into the target repo:

.github/workflows/*.yml from this repository.

helm/app-chart/ (or adapt to your use case).

Update the following as needed:

values.yaml (service name, image repository, ingress, resources, etc.).

Validation step in l2-push-validate-and-build.yml (tests/linters).

Namespace / release name in l3-merge-deploy.yml if needed.

Configure secrets in the target repo:

DOCKERHUB_USERNAME

DOCKERHUB_TOKEN

Open a PR → L1 runs.

Push to branches → L2 runs (build + optional push).

Merge to main → L3 creates a kind cluster and deploys via Helm.

2. Automated onboarding (optional)
This repository is intended to be used together with a separate
onboarding repository, which:

Accepts a target_repo input.

Clones the target repository.

Copies workflows and the Helm chart from this templates repository.

Opens a Pull Request in the target repository with the CI/CD setup.

(See the onboarding repository for implementation details.)

Future improvements
Support for additional registries (GHCR, ECR, GCR).

Environment-specific values (dev/stage/prod).

Integration with a real managed Kubernetes cluster (AKS/EKS/GKE).

Promotion pipelines between environments.