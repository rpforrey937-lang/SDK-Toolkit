# 🚀 Quick Deployment Reference

## Current Status: ✅ Running Locally

Services are running on your machine:
- **Gateway**: http://localhost:8000
- **MCP Server**: http://localhost:9000

## Commands

### View Services
```bash
docker-compose ps
docker-compose logs -f
```

### Stop Services
```bash
docker-compose down
```

### Restart Services
```bash
docker-compose restart
```

---

## Deploy to Cloud (Choose One)

### 1️⃣ Google Cloud Run (Easiest)
```bash
chmod +x deploy-gcloud.sh
./deploy-gcloud.sh YOUR_PROJECT_ID us-central1 v1.0.0
```
**Time:** 5 minutes | **Cost:** $0-3/month

### 2️⃣ AWS ECS Fargate
```bash
chmod +x deploy-ecs.sh
./deploy-ecs.sh production v1.0.0
```
**Time:** 15 minutes | **Cost:** $5-30/month

### 3️⃣ Kubernetes
```bash
chmod +x deploy-k8s.sh
./deploy-k8s.sh agentic-commerce docker.io v1.0.0
```
**Time:** 10 minutes | **Cost:** $20-100/month

### 4️⃣ Production Docker Compose
```bash
docker-compose -f docker-compose.prod.yml up -d
```
**Time:** 3 minutes | **Cost:** Variable

---

## Production Checklist

- [ ] Set environment variables (see `.env.example`)
- [ ] Configure database (PostgreSQL)
- [ ] Set up SSL/TLS certificates
- [ ] Configure domain name
- [ ] Set up monitoring (CloudWatch, Datadog, etc.)
- [ ] Configure backups
- [ ] Set up CI/CD pipeline (GitHub Actions configured)
- [ ] Test DNS and SSL
- [ ] Load test
- [ ] Set up alerts

---

## Testing Deployment

```bash
# Check gateway health
curl https://your-gateway.com/health

# Check MCP health
curl https://your-mcp.com/health

# Create token
curl -X POST https://your-gateway.com/token \
  -H "Content-Type: application/json" \
  -d '{"user": "test", "amount": 100}'

# Process checkout
curl -X POST https://your-gateway.com/checkout \
  -H "Content-Type: application/json" \
  -d '{
    "merchant": "woocommerce",
    "token": "tok_xxx",
    "items": [{"product": "test", "price": 100}]
  }'
```

---

## Monitoring

### Local
```bash
docker stats  # View container resource usage
docker logs -f [container_name]
```

### AWS ECS
```bash
aws ecs describe-services --cluster agentic-commerce --services agentic-gateway
aws logs tail /ecs/agentic-gateway --follow
```

### Google Cloud Run
```bash
gcloud run services describe agentic-gateway --region us-central1
gcloud logging read "resource.type=cloud_run_revision" --limit 50
```

### Kubernetes
```bash
kubectl get pods -n agentic-commerce
kubectl logs -f deployment/agentic-gateway -n agentic-commerce
kubectl top pods -n agentic-commerce
```

---

## Troubleshooting

### Services won't start
```bash
docker-compose logs -f
docker events
```

### Connection refused
- Make sure services are running: `docker-compose ps`
- Wait 10 seconds for startup

### High memory usage
```bash
docker stats
# Reduce worker count in production Dockerfile
```

### Slow responses
```bash
# Check resource limits
docker inspect [container_id] | grep -A 5 HostConfig

# Scale horizontally (increase replicas)
```

---

## Next Steps

1. Choose a cloud provider
2. Run the deployment script
3. Configure domain/SSL
4. Set up monitoring
5. Deploy WooCommerce/Shopify plugins
6. Test end-to-end

For detailed instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)
