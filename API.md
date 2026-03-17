# API Documentation

## Base URLs

- **Gateway**: `http://localhost:8000`
- **MCP Server**: `http://localhost:9000`
- **Shopify App**: `http://localhost:3000`

---

## Gateway API

### Health Check

**Request:**
```
GET /health
```

**Response:**
```json
{
  "status": "ok"
}
```

---

### Create Token

**Request:**
```
POST /token
Content-Type: application/json

{
  "user": "customer123",
  "amount": 100.00
}
```

**Parameters:**
- `user` (string, required): User or agent identifier
- `amount` (number, required): Token amount limit in dollars

**Response:**
```json
{
  "token": "tok_550e8400-e29b-41d4-a716-446655440000",
  "limit": 100.00,
  "user": "customer123"
}
```

**Status Codes:**
- `200 OK` - Token created successfully
- `400 Bad Request` - Missing or invalid parameters

---

### Get Token Status

**Request:**
```
GET /token/{token_id}
```

**Parameters:**
- `token_id` (path, required): The token ID

**Response:**
```json
{
  "token": "tok_550e8400-e29b-41d4-a716-446655440000",
  "user": "customer123",
  "limit": 100.00,
  "used": 50.00,
  "remaining": 50.00
}
```

**Status Codes:**
- `200 OK` - Token found
- `404 Not Found` - Token does not exist

---

### Process Checkout

**Request:**
```
POST /checkout
Content-Type: application/json

{
  "merchant": "woocommerce",
  "token": "tok_550e8400-e29b-41d4-a716-446655440000",
  "items": [
    {
      "product": "running shoes",
      "price": 80.00,
      "quantity": 1
    },
    {
      "product": "socks",
      "price": 10.00,
      "quantity": 2
    }
  ]
}
```

**Parameters:**
- `merchant` (string, required): Merchant identifier (e.g., "woocommerce", "shopify")
- `token` (string, required): The agentic payment token
- `items` (array, required): List of items to purchase

**Item Schema:**
- `product` (string): Product name
- `price` (number): Item price
- `quantity` (number): Quantity

**Response:**
```json
{
  "status": "success",
  "order_id": "ord_550e8400-e29b-41d4-a716-446655440000",
  "merchant": "woocommerce",
  "items": [...],
  "total": 100.00
}
```

**Status Codes:**
- `200 OK` - Checkout processed
- `400 Bad Request` - Invalid request
- `402 Payment Required` - Insufficient token balance
- `404 Not Found` - Token not found

---

## MCP Server API

### List Available Tools

**Request:**
```
GET /tools
```

**Response:**
```json
{
  "tools": [
    {
      "name": "create_token",
      "description": "Create a new agentic payment token",
      "params": {
        "user": "User or agent identifier",
        "amount": "Token amount limit"
      }
    },
    {
      "name": "checkout",
      "description": "Process checkout with an agentic token",
      "params": {
        "merchant": "Merchant identifier",
        "token": "The agentic payment token",
        "items": "List of items to purchase"
      }
    },
    {
      "name": "get_token_status",
      "description": "Get remaining balance and status of a token",
      "params": {
        "token": "The agentic payment token"
      }
    }
  ]
}
```

---

### Create Token (via MCP)

**Request:**
```
POST /create_token
Content-Type: application/json

{
  "user": "agent123",
  "amount": 250.00
}
```

**Response:**
```json
{
  "token": "tok_...",
  "limit": 250.00,
  "user": "agent123"
}
```

---

### Process Checkout (via MCP)

**Request:**
```
POST /checkout
Content-Type: application/json

{
  "merchant": "shopify",
  "token": "tok_...",
  "items": [...]
}
```

**Response:**
```json
{
  "status": "success",
  "order_id": "ord_...",
  "merchant": "shopify"
}
```

---

### Get Token Status (via MCP)

**Request:**
```
GET /token_status/{token_id}
```

**Response:**
```json
{
  "token": "tok_...",
  "user": "agent123",
  "limit": 250.00,
  "used": 0.00,
  "remaining": 250.00
}
```

---

## Shopify App API

### Health Check

**Request:**
```
GET /health
```

**Response:**
```json
{
  "status": "ok"
}
```

---

### Agent Checkout

**Request:**
```
POST /agent-checkout
Content-Type: application/json

{
  "token": "tok_...",
  "items": [
    {
      "product": "jacket",
      "price": 150.00
    }
  ],
  "merchantId": "gid://shopify/Shop/1"
}
```

**Response:**
```json
{
  "status": "success",
  "order_id": "ord_..."
}
```

---

### Create Token

**Request:**
```
POST /create-token
Content-Type: application/json

{
  "user": "customer456",
  "amount": 200.00
}
```

**Response:**
```json
{
  "success": true,
  "token": "tok_...",
  "limit": 200.00
}
```

---

### Get Token Status

**Request:**
```
GET /token-status/{tokenId}
```

**Response:**
```json
{
  "token": "tok_...",
  "user": "customer456",
  "limit": 200.00,
  "used": 0.00,
  "remaining": 200.00
}
```

---

## Error Responses

All endpoints may return error responses in the following format:

```json
{
  "status": "error",
  "message": "Error description"
}
```

Common error codes:
- `400` - Bad Request: Missing or invalid parameters
- `401` - Unauthorized: Invalid API key
- `404` - Not Found: Resource not found
- `402` - Payment Required: Insufficient balance
- `500` - Internal Server Error: Server-side error

---

## Authentication

For production use, implement bearer token authentication:

```
Authorization: Bearer <your-api-key>
```

---

## Rate Limiting

API calls are not currently rate-limited in this development version. 

For production deployment, implement rate limiting:
- 100 requests per minute per IP
- 1000 requests per hour per API key

---

## Webhooks

Future version will support webhooks for:
- Token creation events
- Checkout completion events
- Payment failure events

---

## Versioning

Current API version: **v1**

Future versions will be available at `/v2`, `/v3`, etc.
