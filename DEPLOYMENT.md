# 🚀 Deployment Guide - Agentic Commerce Toolkit

## Status: ✅ Deployed Locally

Your services are now running and tested!

```
✓ Gateway Service    → http://localhost:8000
✓ MCP Server         → http://localhost:9000
✓ Example tested     → Autonomous checkout working
```

---

## Local Deployment (Running)

### Services

```bash
# View running containers
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart services
docker-compose restart

# Rebuild and restart
docker-compose up --build
```

### Test Services

```bash
# Health check gateway
curl http://localhost:8000/health

# Health check MCP
curl http://localhost:9000/health

# Create a token
curl -X POST http://localhost:8000/token \
  -H "Content-Type: application/json" \
  -d '{"user": "test", "amount": 100}'

# Run example script
python3 example_agent.py
```

---

## Cloud Deployment Options

### 🔴 **Option A: Docker Hub (Recommended for Quick Deployment)**

#### Step 1: Push Images to Docker Hub

```bash
# Login to Docker Hub
docker login

# Tag images
docker tag sdk-toolkit-gateway:latest YOUR_USERNAME/agentic-gateway:latest
docker tag sdk-toolkit-mcp:latest YOUR_USERNAME/agentic-mcp:latest

# Push images
docker push YOUR_USERNAME/agentic-gateway:latest
docker push YOUR_USERNAME/agentic-mcp:latest
```

#### Step 2: Deploy to Cloud Provider

See options below (AWS, Google Cloud, Azure, Heroku)

---

### 🔵 **Option B: AWS Elastic Container Service (ECS)**

#### 1. Create ECR Repositories

```bash
# Login to AWS ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com

# Create repositories
aws ecr create-repository --repository-name agentic-gateway --region us-east-1
aws ecr create-repository --repository-name agentic-mcp --region us-east-1
```

#### 2. Push Images

```bash
# Tag and push gateway
docker tag sdk-toolkit-gateway:latest <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/agentic-gateway:latest
docker push <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/agentic-gateway:latest

# Tag and push MCP
docker tag sdk-toolkit-mcp:latest <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/agentic-mcp:latest
docker push <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/agentic-mcp:latest
```

#### 3. Create ECS Task Definition

Create `task-definition.json`:

```json
{
  "family": "agentic-commerce",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "gateway",
      "image": "<ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/agentic-gateway:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "hostPort": 8000,
          "protocol": "tcp"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/agentic-gateway",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    },
    {
      "name": "mcp",
      "image": "<ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/agentic-mcp:latest",
      "portMappings": [
        {
          "containerPort": 9000,
          "hostPort": 9000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "GATEWAY_URL",
          "value": "http://gateway:8000"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/agentic-mcp",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

#### 4. Create ECS Service

```bash
# Register task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json --region us-east-1

# Create ECS cluster
aws ecs create-cluster --cluster-name agentic-commerce --region us-east-1

# Create service
aws ecs create-service \
  --cluster agentic-commerce \
  --service-name agentic-gateway \
  --task-definition agentic-commerce \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}" \
  --region us-east-1
```

---

### 🟢 **Option C: Google Cloud Run (Easiest Serverless)**

#### 1. Install gcloud CLI

```bash
# Install Google Cloud SDK
curl https://sdk.cloud.google.com | bash

# Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

#### 2. Build and Push to Google Artifact Registry

```bash
# Create artifact registry repository
gcloud artifacts repositories create agentic-commerce \
  --repository-format=docker \
  --location=us-central1

# Configure Docker auth
gcloud auth configure-docker us-central1-docker.pkg.dev

# Build and push gateway
docker build -t us-central1-docker.pkg.dev/YOUR_PROJECT_ID/agentic-commerce/gateway:latest ./gateway
docker push us-central1-docker.pkg.dev/YOUR_PROJECT_ID/agentic-commerce/gateway:latest

# Build and push MCP
docker build -t us-central1-docker.pkg.dev/YOUR_PROJECT_ID/agentic-commerce/mcp:latest ./mcp-server
docker push us-central1-docker.pkg.dev/YOUR_PROJECT_ID/agentic-commerce/mcp:latest
```

#### 3. Deploy to Cloud Run

```bash
# Deploy gateway
gcloud run deploy agentic-gateway \
  --image us-central1-docker.pkg.dev/YOUR_PROJECT_ID/agentic-commerce/gateway:latest \
  --platform managed \
  --region us-central1 \
  --memory 512Mi \
  --cpu 1 \
  --allow-unauthenticated

# Deploy MCP server
gcloud run deploy agentic-mcp \
  --image us-central1-docker.pkg.dev/YOUR_PROJECT_ID/agentic-commerce/mcp:latest \
  --platform managed \
  --region us-central1 \
  --memory 512Mi \
  --cpu 1 \
  --allow-unauthenticated \
  --set-env-vars GATEWAY_URL="https://YOUR_GATEWAY_URL"
```

Your services will be available at generated URLs like:
- Gateway: `https://agentic-gateway-xxxxx.run.app`
- MCP: `https://agentic-mcp-xxxxx.run.app`

---

### 🟡 **Option D: Microsoft Azure Container Instances**

#### 1. Create Azure Container Registry

```bash
# Create resource group
az group create --name agentic-rg --location eastus

# Create ACR
az acr create --resource-group agentic-rg --name agenticacr --sku Basic
```

#### 2. Build and Push Images

```bash
# Login to ACR
az acr login --name agenticacr

# Build and push gateway
az acr build --registry agenticacr --image agentic-gateway:latest ./gateway

# Build and push MCP
az acr build --registry agenticacr --image agentic-mcp:latest ./mcp-server
```

#### 3. Deploy to ACI

```bash
# Deploy gateway
az container create \
  --resource-group agentic-rg \
  --name agentic-gateway \
  --image agenticacr.azurecr.io/agentic-gateway:latest \
  --cpu 1 \
  --memory 0.5 \
  --ports 8000 \
  --registry-login-server agenticacr.azurecr.io \
  --registry-username <username> \
  --registry-password <password>

# Deploy MCP
az container create \
  --resource-group agentic-rg \
  --name agentic-mcp \
  --image agenticacr.azurecr.io/agentic-mcp:latest \
  --cpu 1 \
  --memory 0.5 \
  --ports 9000 \
  --environment-variables GATEWAY_URL=http://agentic-gateway:8000 \
  --registry-login-server agenticacr.azurecr.io \
  --registry-username <username> \
  --registry-password <password>
```

---

### 🟣 **Option E: Heroku (Free Tier Available)**

#### 1. Install Heroku CLI

```bash
curl https://cli-assets.heroku.com/install.sh | sh
heroku login
```

#### 2. Create heroku.yml

```yaml
build:
  docker:
    web: Dockerfile
```

#### 3. Deploy

```bash
# Create Heroku app for gateway
heroku create agentic-gateway
heroku stack:set container

# Deploy
git push heroku main

# Repeat for MCP server
heroku create agentic-mcp
# ... deploy
```

---

### 🔶 **Option F: Kubernetes (Production-Grade)**

#### 1. Create Kubernetes Manifests

**gateway-deployment.yaml:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agentic-gateway
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
        image: YOUR_REGISTRY/agentic-gateway:latest
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
---
apiVersion: v1
kind: Service
metadata:
  name: agentic-gateway
spec:
  selector:
    app: agentic-gateway
  ports:
  - port: 8000
    targetPort: 8000
  type: LoadBalancer
```

**mcp-deployment.yaml:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agentic-mcp
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
        image: YOUR_REGISTRY/agentic-mcp:latest
        ports:
        - containerPort: 9000
        env:
        - name: GATEWAY_URL
          value: "http://agentic-gateway:8000"
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
---
apiVersion: v1
kind: Service
metadata:
  name: agentic-mcp
spec:
  selector:
    app: agentic-mcp
  ports:
  - port: 9000
    targetPort: 9000
  type: LoadBalancer
```

#### 2. Deploy to Kubernetes

```bash
# Create namespace
kubectl create namespace agentic-commerce

# Apply deployments
kubectl apply -f gateway-deployment.yaml -n agentic-commerce
kubectl apply -f mcp-deployment.yaml -n agentic-commerce

# Check status
kubectl get pods -n agentic-commerce
kubectl get services -n agentic-commerce
```

---

## Production Configuration

### Environment Variables

Create `.env` for your deployment:

```bash
# Service URLs
GATEWAY_URL=https://your-gateway-domain.com
MCP_URL=https://your-mcp-domain.com

# Database (optional)
DATABASE_URL=postgresql://user:pass@db-host:5432/agentic_commerce

# Logging
LOG_LEVEL=INFO

# Security
API_KEY_SECRET=your-secret-key
ALLOWED_ORIGINS=https://yourdomain.com
```

### Database (Optional)

Add PostgreSQL to your deployment for persistent token storage:

```yaml
# AWS RDS, Google Cloud SQL, or managed database
services:
  db:
    image: postgres:14
    environment:
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

### Monitoring

Add monitoring services:

```yaml
# Prometheus for metrics
prometheus:
  image: prom/prometheus:latest
  ports:
    - "9090:9090"

# Grafana for dashboards
grafana:
  image: grafana/grafana:latest
  ports:
    - "3000:3000"
```

---

## Quick Deployment Comparison

| Option | Setup Time | Cost | Scalability | Best For |
|--------|-----------|------|-------------|----------|
| **Local Docker** | 2 min | Free | Limited | Development |
| **Google Cloud Run** | 10 min | Pay-per-use | Auto | Production |
| **AWS ECS Fargate** | 15 min | Low | Auto | Enterprise |
| **Kubernetes** | 20 min | Varies | Unlimited | High-scale |
| **Heroku** | 5 min | Low | Limited | MVP |
| **Azure ACI** | 10 min | Low | Limited | Microsoft stack |

---

## Monitoring and Health Checks

### Docker Health Check

```bash
# View container health
docker inspect sdk-toolkit-gateway-1 | grep -A 5 Health
```

### API Health Endpoints

```bash
# Gateway
curl https://your-gateway.com/health

# MCP Server
curl https://your-mcp.com/health

# Get token status
curl https://your-gateway.com/token/tok_xxx
```

### Logs

```bash
# Local docker-compose
docker-compose logs -f gateway
docker-compose logs -f mcp

# Kubernetes
kubectl logs -f deployment/agentic-gateway -n agentic-commerce
kubectl logs -f deployment/agentic-mcp -n agentic-commerce

# AWS CloudWatch
aws logs tail /ecs/agentic-gateway --follow

# Google Cloud
gcloud logging read "resource.type=cloud_run_revision" --limit 50 --format json
```

---

## Support & Next Steps

✅ **Completed:**
- Local deployment running
- Example test successful
- Services healthy

📋 **Next Steps:**
1. Configure production environment variables
2. Set up database (optional)
3. Choose cloud deployment option
4. Configure domain and SSL
5. Set up monitoring and alerts
6. Deploy WooCommerce/Shopify plugins

Need help with any specific deployment? Let me know!
