#!/bin/bash

set -e

# Check prerequisites
command -v kind >/dev/null 2>&1 || { echo "kind is required but not installed. Aborting."; exit 1; }
command -v kubectl >/dev/null 2>&1 || { echo "kubectl is required but not installed. Aborting."; exit 1; }
command -v docker >/dev/null 2>&1 || { echo "docker is required but not installed. Aborting."; exit 1; }

# Create Kind cluster
echo "Creating Kind cluster..."
kind create cluster --config k8s/kind-config.yaml --name otel-fga

# Build and load Docker image for the app
echo "Building Docker image for the app..."
docker build -t app:latest .
kind load docker-image app:latest --name otel-fga

# Apply Kustomize manifests excluding openfga-init-job
echo "Applying Kustomize manifests (excluding openfga-init-job)..."
kubectl apply -k k8s/base --selector=app!=openfga-init,app!=app

# Wait for openfga deployment to be ready
echo "Waiting for OpenFGA deployment to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/openfga -n otel-fga

# Apply openfga-init-job
echo "Applying openfga-init-job..."
kubectl apply -f k8s/base/openfga-init-job.yaml

# Wait for OpenFGA init job to complete
echo "Waiting for OpenFGA init job to complete..."
kubectl wait --for=condition=complete --timeout=300s job/openfga-init -n otel-fga

# Apply app deployment
echo "Applying app deployment..."
kubectl apply -f k8s/base/app-deployment.yaml

# Wait for deployments to be ready
echo "Waiting for deployments to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/otel-collector -n otel-fga
kubectl wait --for=condition=available --timeout=300s deployment/app -n otel-fga
kubectl wait --for=condition=available --timeout=300s deployment/prometheus -n otel-fga
kubectl wait --for=condition=available --timeout=300s deployment/grafana -n otel-fga

echo "Cluster setup complete!"
echo "Access the app at http://localhost:8000/check?user=user:alice&resource=document:123"
echo "Access Grafana at http://localhost:3000 (admin/admin)"
echo "Access OpenFGA at http://localhost:8080"
echo "Access Prometheus at http://localhost:9091"