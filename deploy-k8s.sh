#!/bin/bash

# Kubernetes Deployment Script
# Usage: ./deploy-k8s.sh [namespace] [registry] [version]

set -e

NAMESPACE=${1:-agentic-commerce}
REGISTRY=${2:-docker.io}
VERSION=${3:-latest}

echo "🚀 Deploying Agentic Commerce to Kubernetes"
echo "Namespace: $NAMESPACE"
echo "Registry: $REGISTRY"
echo "Version: $VERSION"

# Create namespace
echo ""
echo "📋 Creating namespace..."
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Build and push images
echo ""
echo "📦 Building and pushing images..."
docker build -t $REGISTRY/agentic-gateway:$VERSION ./gateway
docker push $REGISTRY/agentic-gateway:$VERSION
echo "✓ Gateway image pushed"

docker build -t $REGISTRY/agentic-mcp:$VERSION ./mcp-server
docker push $REGISTRY/agentic-mcp:$VERSION
echo "✓ MCP image pushed"

# Create ConfigMap for environment variables
echo ""
echo "⚙️  Creating ConfigMap..."
kubectl create configmap agentic-config \
  --from-literal=GATEWAY_URL=http://agentic-gateway:8000 \
  --from-literal=LOG_LEVEL=INFO \
  --namespace=$NAMESPACE \
  --dry-run=client -o yaml | kubectl apply -f -

# Create Deployment for Gateway
echo ""
echo "🚀 Deploying Gateway..."
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agentic-gateway
  namespace: $NAMESPACE
spec:
  replicas: 3
  selector:
    matchLabels:
      app: agentic-gateway
  template:
    metadata:
      labels:
        app: agentic-gateway
    spec:
      containers:
      - name: gateway
        image: $REGISTRY/agentic-gateway:$VERSION
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: agentic-gateway
  namespace: $NAMESPACE
spec:
  selector:
    app: agentic-gateway
  ports:
  - port: 8000
    targetPort: 8000
  type: LoadBalancer
EOF

# Create Deployment for MCP
echo "🚀 Deploying MCP Server..."
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agentic-mcp
  namespace: $NAMESPACE
spec:
  replicas: 2
  selector:
    matchLabels:
      app: agentic-mcp
  template:
    metadata:
      labels:
        app: agentic-mcp
    spec:
      containers:
      - name: mcp
        image: $REGISTRY/agentic-mcp:$VERSION
        ports:
        - containerPort: 9000
        env:
        - name: GATEWAY_URL
          valueFrom:
            configMapKeyRef:
              name: agentic-config
              key: GATEWAY_URL
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 9000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 9000
          initialDelaySeconds: 10
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: agentic-mcp
  namespace: $NAMESPACE
spec:
  selector:
    app: agentic-mcp
  ports:
  - port: 9000
    targetPort: 9000
  type: LoadBalancer
EOF

echo ""
echo "✅ Deployment complete!"
echo ""
echo "View deployment status:"
echo "kubectl get deployments -n $NAMESPACE"
echo "kubectl get pods -n $NAMESPACE"
echo "kubectl get services -n $NAMESPACE"
echo ""
echo "View logs:"
echo "kubectl logs -f deployment/agentic-gateway -n $NAMESPACE"
echo "kubectl logs -f deployment/agentic-mcp -n $NAMESPACE"
