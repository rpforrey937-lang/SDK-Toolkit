# Installation Guide

## Prerequisites

- Python 3.7+
- Node.js 14+ (for Shopify app)
- Docker & Docker Compose (optional, for containerized setup)
- WordPress 5.0+ (for WooCommerce plugin)

## Quick Start with Docker

```bash
docker-compose up
```

This will start:
- Gateway on http://localhost:8000
- MCP Server on http://localhost:9000

## Manual Installation

### 1. Python SDK

```bash
cd sdk-python
pip install -e .
```

### 2. Agent Commerce Gateway

```bash
cd gateway
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

### 3. MCP Server

```bash
cd mcp-server
pip install -r requirements.txt
uvicorn server:app --host 0.0.0.0 --port 9000
```

### 4. Shopify App

```bash
cd shopify-app
npm install
npm start
```

The app will run on http://localhost:3000

### 5. WooCommerce Plugin

1. Copy the `woocommerce-plugin` folder to:
   ```
   wp-content/plugins/agentic-pay/
   ```

2. Activate the plugin in WordPress admin dashboard

3. Configure the gateway URL in WooCommerce settings:
   - Go to WooCommerce > Settings > Payments
   - Enable "Agentic Pay"
   - Set Gateway URL to your gateway instance (default: http://localhost:8000)

## Environment Variables

### Gateway

```bash
export PYTHONUNBUFFERED=1
```

### MCP Server

```bash
export GATEWAY_URL=http://localhost:8000
export PYTHONUNBUFFERED=1
```

### Shopify App

```bash
export GATEWAY_URL=http://localhost:8000
export PORT=3000
```

## Testing the Installation

### Test with Python SDK

```bash
python example_agent.py
```

### Test with cURL

Create a token:
```bash
curl -X POST http://localhost:8000/token \
  -H "Content-Type: application/json" \
  -d '{"user": "test", "amount": 100}'
```

Check token status:
```bash
curl http://localhost:8000/token/tok_<token_id>
```

Process checkout:
```bash
curl -X POST http://localhost:8000/checkout \
  -H "Content-Type: application/json" \
  -d '{
    "merchant": "woocommerce",
    "token": "tok_<token_id>",
    "items": [{"product": "test", "price": 50}]
  }'
```

## Troubleshooting

### Port already in use

Change the port in the respective service:

```bash
# Gateway on different port
uvicorn app:app --port 8001

# MCP on different port
uvicorn server:app --port 9001

# Shopify app on different port
PORT=3001 npm start
```

### Import errors

Ensure you're in a virtual environment and dependencies are installed:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Docker issues

Clear Docker cache and rebuild:

```bash
docker-compose down
docker system prune
docker-compose up --build
```

## Next Steps

- Read [USAGE.md](USAGE.md) for API usage examples
- Check [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- Review the [README.md](README.md) for project overview
