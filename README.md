# Agentic Commerce Toolkit

Open-source toolkit for enabling AI agents to perform secure autonomous purchases using tokenized payments.

Includes:

- Python Agent SDK
- Agent Commerce Gateway
- MCP Server for AI tools
- WooCommerce payment plugin
- Shopify checkout integration

## Features

- Agent token payments
- Autonomous checkout APIs
- AI agent tooling
- Merchant plugins

## Quick Start

```bash
docker-compose up
```

### SDK example:

```python
from agentic_sdk import AgentClient

agent = AgentClient(api_key="test")

token = agent.create_token(user="123", amount=50)

agent.checkout(
    merchant="demo-store",
    token=token,
    items=[{"product":"shoe","price":50}]
)
```

## Project Structure

```
agentic-commerce-toolkit/
├── README.md
├── docker-compose.yml
├── sdk-python/
│   ├── agentic_sdk/
│   │   ├── __init__.py
│   │   ├── client.py
│   │   ├── token_manager.py
│   │   ├── checkout.py
│   │   └── config.py
│   └── setup.py
├── mcp-server/
│   ├── server.py
│   └── requirements.txt
├── gateway/
│   ├── app.py
│   └── requirements.txt
├── woocommerce-plugin/
│   ├── agentic-pay.php
│   └── class-agentic-gateway.php
└── shopify-app/
    ├── server.js
    ├── package.json
    └── routes/
        └── agentCheckout.js
```

## Components

### Python SDK
Python client for agents to interact with the commerce gateway and create tokenized payments.

### Agent Commerce Gateway
FastAPI-based gateway handling token generation and checkout processing.

### MCP Server
Model Context Protocol server providing agent tooling for autonomous commerce operations.

### WooCommerce Plugin
WordPress payment gateway plugin for accepting agentic payments in WooCommerce stores.

### Shopify App
Shopify app integration for enabling agent-based checkout on Shopify stores.

## Installation & Running

1. **With Docker:**
   ```bash
   docker-compose up
   ```

2. **Manual Setup:**
   - Gateway: `cd gateway && pip install -r requirements.txt && uvicorn app:app`
   - MCP Server: `cd mcp-server && pip install -r requirements.txt && uvicorn server:app --port 9000`
   - Python SDK: `cd sdk-python && pip install -e .`
   - Shopify App: `cd shopify-app && npm install && npm start`

## Deploying on Railway

This repository includes a `railway.json` configuration and Dockerfiles that are compatible with Railway deployments (Railway provides the `PORT` env var at runtime).

```bash
# Install Railway CLI: https://railway.app
railway init
railway up
```

Railway will build the `gateway` and `mcp` services using their respective Dockerfiles and route incoming requests to the appropriate service ports.

## API Endpoints

### Gateway (Port 8000)
- `POST /token` - Create agent payment token
- `POST /checkout` - Process checkout with token

### MCP Server (Port 9000)
- `GET /tools` - List available agent tools
- `POST /create_token` - Create token via MCP
- `POST /checkout` - Checkout via MCP

### Shopify App (Port 3000)
- `POST /agent-checkout` - Process Shopify checkout with agent token

## License

MIT