# Check prerequisites
if (-not (Get-Command kind -ErrorAction SilentlyContinue)) {
    Write-Error "kind is required but not installed. Aborting."
    exit 1
}
if (-not (Get-Command kubectl -ErrorAction SilentlyContinue)) {
    Write-Error "kubectl is required but not installed. Aborting."
    exit 1
}
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Error "docker is required but not installed. Aborting."
    exit 1
}

# Create Kind cluster
Write-Host "Creating Kind cluster..."
kind create cluster --config k8s/kind-config.yaml --name otel-fga

# Build and load Docker image for the app
Write-Host "Building Docker image for the app..."
docker build -t app:latest .
kind load docker-image app:latest --name otel-fga

# Apply Kustomize manifests excluding openfga-init-job
Write-Host "Applying Kustomize manifests (excluding openfga-init-job)..."
kubectl apply -k k8s/base --selector=app!=openfga-init,app!=app

# Wait for openfga deployment to be ready
Write-Host "Waiting for OpenFGA deployment to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/openfga -n otel-fga

# Apply openfga-init-job
Write-Host "Applying openfga-init-job..."
kubectl apply -f k8s/base/openfga-init-job.yaml

# Wait for OpenFGA init job to complete
Write-Host "Waiting for OpenFGA init job to complete..."
kubectl wait --for=condition=complete --timeout=300s job/openfga-init -n otel-fga

# Apply app deployment
Write-Host "Applying app deployment..."
kubectl apply -f k8s/base/app-deployment.yaml

# Wait for deployments to be ready
Write-Host "Waiting for deployments to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/otel-collector -n otel-fga
kubectl wait --for=condition=available --timeout=300s deployment/app -n otel-fga
kubectl wait --for=condition=available --timeout=300s deployment/prometheus -n otel-fga
kubectl wait --for=condition=available --timeout=300s deployment/grafana -n otel-fga
kubectl wait --for=condition=available --timeout=300s deployment/jaeger -n otel-fga

Write-Host "Cluster setup complete!"
Write-Host "Access the app at http://localhost:8000/check?user=user:alice&resource=document:123"
Write-Host "Access Grafana at http://localhost:3000 (admin/admin)"
Write-Host "Access OpenFGA at http://localhost:8080"
Write-Host "Access Prometheus at http://localhost:9091"
Write-Host "Access Jaeger at http://localhost:16686"