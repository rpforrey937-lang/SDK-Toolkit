#!/bin/bash

# Google Cloud Run Deployment Script
# Usage: ./deploy-gcloud.sh [project-id] [region] [version]

set -e

PROJECT_ID=${1:-your-project-id}
REGION=${2:-us-central1}
VERSION=${3:-latest}

echo "🚀 Deploying Agentic Commerce to Google Cloud Run"
echo "Project: $PROJECT_ID"
echo "Region: $REGION"
echo "Version: $VERSION"

# Set project
gcloud config set project $PROJECT_ID

# Artifact Registry
AR_REPO="$REGION-docker.pkg.dev/$PROJECT_ID/agentic-commerce"

echo ""
echo "📦 Building and pushing Docker images..."

# Configure Docker auth
gcloud auth configure-docker $REGION-docker.pkg.dev

# Build and push gateway
docker build -t "$AR_REPO/gateway:$VERSION" ./gateway
docker push "$AR_REPO/gateway:$VERSION"
echo "✓ Gateway image pushed"

# Build and push MCP
docker build -t "$AR_REPO/mcp:$VERSION" ./mcp-server
docker push "$AR_REPO/mcp:$VERSION"
echo "✓ MCP image pushed"

echo ""
echo "🚀 Deploying to Cloud Run..."

# Deploy gateway
gcloud run deploy agentic-gateway \
  --image="$AR_REPO/gateway:$VERSION" \
  --platform=managed \
  --region=$REGION \
  --memory=512Mi \
  --cpu=1 \
  --allow-unauthenticated \
  --timeout=60

# Get gateway URL
GATEWAY_URL=$(gcloud run services describe agentic-gateway --region=$REGION --format='value(status.url)')
echo "✓ Gateway deployed: $GATEWAY_URL"

# Deploy MCP
gcloud run deploy agentic-mcp \
  --image="$AR_REPO/mcp:$VERSION" \
  --platform=managed \
  --region=$REGION \
  --memory=512Mi \
  --cpu=1 \
  --allow-unauthenticated \
  --timeout=60 \
  --set-env-vars GATEWAY_URL=$GATEWAY_URL

# Get MCP URL
MCP_URL=$(gcloud run services describe agentic-mcp --region=$REGION --format='value(status.url)')
echo "✓ MCP deployed: $MCP_URL"

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Service URLs:"
echo "  Gateway: $GATEWAY_URL"
echo "  MCP: $MCP_URL"
echo ""
echo "View logs:"
echo "  Cloud Run: gcloud run logs read agentic-gateway --region=$REGION"
