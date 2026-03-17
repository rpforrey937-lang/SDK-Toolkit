# Docker Deployment Guide

## Development with Docker

### Quick Start

```bash
docker-compose up
```

This will start:
- **Agentic Commerce Gateway** on http://localhost:8000
- **MCP Server** on http://localhost:9000

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f gateway
docker-compose logs -f mcp
```

### Stop Services

```bash
docker-compose down
```

### Rebuild Images

```bash
docker-compose up --build
```

---

## Production Deployment

### Build Images

```bash
docker build -t agentic-gateway:latest ./gateway
docker build -t agentic-mcp:latest ./mcp-server
```

### Push to Registry

```bash
docker tag agentic-gateway:latest your-registry/agentic-gateway:latest
docker push your-registry/agentic-gateway:latest

docker tag agentic-mcp:latest your-registry/agentic-mcp:latest
docker push your-registry/agentic-mcp:latest
```

### Run Individual Services

#### Gateway Service

```bash
docker run -d \
  -p 8000:8000 \
  -e PYTHONUNBUFFERED=1 \
  --name agentic-gateway \
  agentic-gateway:latest
```

#### MCP Service

```bash
docker run -d \
  -p 9000:9000 \
  -e GATEWAY_URL=http://gateway:8000 \
  --link agentic-gateway:gateway \
  --name agentic-mcp \
  agentic-mcp:latest
```

### Using Docker Networks

Create a network for inter-service communication:

```bash
docker network create agentic-network

docker run -d \
  --network agentic-network \
  -p 8000:8000 \
  --name agentic-gateway \
  agentic-gateway:latest

docker run -d \
  --network agentic-network \
  -p 9000:9000 \
  -e GATEWAY_URL=http://agentic-gateway:8000 \
  --name agentic-mcp \
  agentic-mcp:latest
```

---

## Kubernetes Deployment (Optional)

### Create Deployment for Gateway

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agentic-gateway
spec:
  replicas: 2
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
        image: your-registry/agentic-gateway:latest
        ports:
        - containerPort: 8000
        env:
        - name: PYTHONUNBUFFERED
          value: "1"
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "500m"
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

### Create Deployment for MCP Server

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agentic-mcp
spec:
  replicas: 1
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
        image: your-registry/agentic-mcp:latest
        ports:
        - containerPort: 9000
        env:
        - name: GATEWAY_URL
          value: "http://agentic-gateway:8000"
        - name: PYTHONUNBUFFERED
          value: "1"
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "500m"
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

### Deploy to Kubernetes

```bash
kubectl apply -f gateway-deployment.yaml
kubectl apply -f mcp-deployment.yaml

# Check status
kubectl get deployments
kubectl get pods
kubectl get services
```

---

## Health Checks

### Docker Health Check

Add to `docker-compose.yml`:

```yaml
services:
  gateway:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Manual Health Check

```bash
curl http://localhost:8000/health
curl http://localhost:9000/health
```

---

## Environment Variables

Create a `.env` file (see `.env.example`):

```bash
cp .env.example .env
# Edit .env with your values
docker-compose --env-file .env up
```

---

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use a different port in docker-compose.yml
```

### Container Won't Start

```bash
# Check logs
docker-compose logs gateway

# Rebuild
docker-compose down
docker-compose up --build
```

### Network Issues

```bash
# Check network
docker network ls

# Inspect network
docker network inspect agentic-network

# Test connectivity between containers
docker exec agentic-gateway ping agentic-mcp
```

---

## Monitoring with Docker

### View Resource Usage

```bash
docker stats
```

### Save Data with Volumes

```yaml
volumes:
  gateway-data:
  mcp-data:

services:
  gateway:
    volumes:
      - gateway-data:/app/data
```

---

## Security

### Run as Non-root User

```dockerfile
RUN useradd -m appuser
USER appuser
```

### Use .dockerignore

```
__pycache__/
venv/
.env
.git
node_modules/
```

### Scan Images for Vulnerabilities

```bash
docker scan agentic-gateway:latest
```

---

## Next Steps

- Deploy to AWS ECS, Google Cloud Run, or Azure Container Instances
- Set up CI/CD pipeline for automatic builds and deployments
- Configure monitoring and logging (ELK, Prometheus, DataDog)
- Implement auto-scaling based on load
