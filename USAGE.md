# Usage Guide

## Python SDK

### Installation

```bash
cd sdk-python
pip install -e .
```

### Basic Usage

```python
from agentic_sdk import AgentClient

# Initialize client
agent = AgentClient(api_key="your-api-key")

# Create a payment token
token_response = agent.create_token(
    user="customer123",
    amount=100.00
)

token = token_response["token"]
print(f"Created token: {token}")

# Process checkout
order = agent.checkout(
    merchant="woocommerce",
    token=token,
    items=[
        {"product": "shoes", "price": 80.00},
        {"product": "socks", "price": 20.00}
    ]
)

print(f"Order ID: {order['order_id']}")
print(f"Status: {order['status']}")
```

### Advanced Examples

#### Handle Multiple Merchants

```python
# Create token for multiple purchases
token = agent.create_token(user="agent001", amount=500.00)

# Purchase from WooCommerce
woo_order = agent.checkout(
    merchant="woocommerce",
    token=token["token"],
    items=[{"product": "shirt", "price": 30.00}]
)

# Purchase from Shopify
shopify_order = agent.checkout(
    merchant="shopify",
    token=token["token"],
    items=[{"product": "jacket", "price": 100.00}]
)
```

#### Error Handling

```python
from agentic_sdk import AgentClient
import requests

try:
    agent = AgentClient(api_key="key")
    
    token = agent.create_token(user="test", amount=50)
    
    order = agent.checkout(
        merchant="woocommerce",
        token=token["token"],
        items=[{"product": "item", "price": 50}]
    )
    
    if order.get("status") == "success":
        print(f"Order successful: {order['order_id']}")
    else:
        print(f"Order failed: {order.get('message')}")
        
except requests.exceptions.ConnectionError:
    print("Could not connect to gateway")
except Exception as e:
    print(f"Error: {e}")
```

---

## Agent Integration

### With Claude/GPT

Agent systems can use the toolkit to make autonomous purchases. Here's a prompt example:

```
You are a shopping agent. You have access to the following tools:
- create_token(user, amount): Creates a payment token
- checkout(merchant, token, items): Processes a purchase

Task: The user wants to buy running shoes for $80 from our store.

Steps:
1. Create a token for $80
2. Process the checkout with the shoes item
3. Return the order ID to the user
```

### MCP Integration

Access the toolkit through the MCP Server:

```python
import requests

# List available tools
tools = requests.get("http://localhost:9000/tools").json()

# Create token through MCP
token = requests.post(
    "http://localhost:9000/create_token",
    json={"user": "agent", "amount": 100}
).json()

# Checkout through MCP
order = requests.post(
    "http://localhost:9000/checkout",
    json={
        "merchant": "woocommerce",
        "token": token["token"],
        "items": [{"product": "shoes", "price": 80}]
    }
).json()
```

---

## WooCommerce Integration

### Installation

1. Copy `woocommerce-plugin/` to `wp-content/plugins/agentic-pay/`
2. Activate in WordPress admin
3. Configure in WooCommerce > Settings > Payments > Agentic Pay

### Configuration

Set your gateway URL:

```
Gateway URL: http://your-server:8000
```

### Using in Store

Customers can now pay with agentic tokens:

1. Add items to cart
2. Go to checkout
3. Select "Agentic Pay" as payment method
4. Enter their agent token
5. Complete purchase

---

## Shopify Integration

### Installation

1. Upload Shopify app files to your Shopify app server
2. Configure with gateway URL
3. Add payment app to your store

### API Endpoints for Shopify Stores

```bash
# Create token for customer
curl -X POST http://your-server:3000/create-token \
  -H "Content-Type: application/json" \
  -d '{"userId": "cust123", "amount": 150}'

# Process checkout
curl -X POST http://your-server:3000/agent-checkout \
  -H "Content-Type: application/json" \
  -d '{
    "token": "tok_...",
    "items": [{"product": "shirt", "price": 50}],
    "merchantId": "gid://shopify/Shop/1"
  }'

# Check token balance
curl http://your-server:3000/token-status/tok_...
```

---

## cURL Examples

### Create Token

```bash
curl -X POST http://localhost:8000/token \
  -H "Content-Type: application/json" \
  -d '{
    "user": "customer123",
    "amount": 100
  }'
```

### Get Token Status

```bash
curl http://localhost:8000/token/tok_550e8400-e29b-41d4-a716-446655440000
```

### Process Checkout

```bash
curl -X POST http://localhost:8000/checkout \
  -H "Content-Type: application/json" \
  -d '{
    "merchant": "woocommerce",
    "token": "tok_550e8400-e29b-41d4-a716-446655440000",
    "items": [
      {"product": "shoes", "price": 80},
      {"product": "socks", "price": 20}
    ]
  }'
```

---

## Testing

### Run Example Script

```bash
python example_agent.py
```

This demonstrates:
- Creating tokens
- Processing checkouts on multiple platforms
- Error handling

### Run Fake WooCommerce Purchase Agent

This script creates an agentic token and performs a fake checkout for a WooCommerce merchant.

```bash
python woo_fake_purchase_agent.py \
  --gateway-url http://localhost:8000 \
  --api-key demo-key-12345 \
  --user demo-user \
  --amount 49.99 \
  --item "T-shirt:49.99"
```

> Tip: If you have a WooCommerce store with the Agentic Pay plugin installed, you can copy the created token into the checkout page to simulate a real purchase.

### Health Checks

```bash
# Check gateway
curl http://localhost:8000/health

# Check MCP server
curl http://localhost:9000/health

# Check Shopify app
curl http://localhost:3000/health
```

---

## Security Best Practices

1. **Keep API keys confidential** - Use environment variables
2. **Use HTTPS in production** - Never send tokens over HTTP
3. **Validate tokens** - Always verify token status before checkout
4. **Set reasonable limits** - Create tokens with appropriate amount limits
5. **Monitor usage** - Track token creation and checkout patterns
6. **Rate limit** - Implement rate limiting in production
7. **Authenticate requests** - Use bearer tokens for API access

---

## Troubleshooting

### Connection Errors

```
Error: Cannot connect to gateway
```

**Solution:** Ensure gateway is running on port 8000

```bash
# Check running processes
lsof -i :8000

# Start gateway if not running
cd gateway && uvicorn app:app --port 8000
```

### Invalid Token Errors

```
Error: Invalid token
```

**Solution:** Check that token exists and hasn't expired

```bash
# Check token status
curl http://localhost:8000/token/tok_...
```

### Insufficient Balance

```
Error: Insufficient token balance
```

**Solution:** Create a new token with larger amount

```bash
# Create new token
curl -X POST http://localhost:8000/token \
  -d '{"user": "customer", "amount": 500}'
```

### Gateway URL Not Found (WooCommerce)

**Solution:** Configure correct gateway URL in WooCommerce settings

1. Go to WooCommerce > Settings > Payments
2. Click on "Agentic Pay"
3. Update "Gateway URL" field
4. Save changes

---

## Next Steps

- Review [API.md](API.md) for detailed endpoint documentation
- Check [INSTALLATION.md](INSTALLATION.md) for setup instructions
- See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute to the project
