#!/bin/bash

# AWS ECS Deployment Script
# Usage: ./deploy-ecs.sh [environment] [version]

set -e

ENVIRONMENT=${1:-staging}
VERSION=${2:-latest}
AWS_REGION=${AWS_REGION:-us-east-1}

echo "🚀 Deploying Agentic Commerce to AWS ECS"
echo "Environment: $ENVIRONMENT"
echo "Version: $VERSION"
echo "Region: $AWS_REGION"

# Get AWS account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo "AWS Account: $ACCOUNT_ID"

# ECR Repository URLs
GATEWAY_ECR="$ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/agentic-gateway"
MCP_ECR="$ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/agentic-mcp"

echo ""
echo "📦 Building and pushing Docker images..."

# Login to ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin "$ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"

# Build and push gateway
docker build -t "$GATEWAY_ECR:$VERSION" ./gateway
docker push "$GATEWAY_ECR:$VERSION"
echo "✓ Gateway image pushed"

# Build and push MCP
docker build -t "$MCP_ECR:$VERSION" ./mcp-server
docker push "$MCP_ECR:$VERSION"
echo "✓ MCP image pushed"

echo ""
echo "📝 Updating ECS task definitions..."

# Update task definition with new image versions
aws ecs update-service \
  --cluster agentic-commerce-$ENVIRONMENT \
  --service agentic-gateway \
  --force-new-deployment \
  --region $AWS_REGION || echo "Service may not exist yet"

aws ecs update-service \
  --cluster agentic-commerce-$ENVIRONMENT \
  --service agentic-mcp \
  --force-new-deployment \
  --region $AWS_REGION || echo "Service may not exist yet"

echo ""
echo "✅ Deployment initiated!"
echo ""
echo "View deployment status:"
echo "aws ecs describe-services --cluster agentic-commerce-$ENVIRONMENT --services agentic-gateway agentic-mcp --region $AWS_REGION"
