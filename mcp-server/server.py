from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI(title="Agentic MCP Server")

GATEWAY = "http://localhost:8000"


class TokenRequestBody(BaseModel):
    user: str
    amount: float


class CheckoutRequestBody(BaseModel):
    merchant: str
    token: str
    items: list


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/tools")
def list_tools():
    """
    List available agent tools for autonomous commerce operations.

    Returns:
        Available tools and their descriptions
    """
    return {
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
                    "merchant": "Merchant identifier (woocommerce, shopify, etc)",
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


@app.post("/create_token")
def create_token(data: TokenRequestBody):
    """
    Create a new agentic payment token via MCP.

    Args:
        data: Token request with user and amount

    Returns:
        Created token data
    """
    try:
        r = requests.post(
            f"{GATEWAY}/token",
            json=data.dict()
        )

        return r.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/checkout")
def checkout(data: CheckoutRequestBody):
    """
    Process checkout with an agentic token via MCP.

    Args:
        data: Checkout request with merchant, token, and items

    Returns:
        Checkout result with order ID
    """
    try:
        r = requests.post(
            f"{GATEWAY}/checkout",
            json=data.dict()
        )

        return r.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/token_status/{token_id}")
def get_token_status(token_id: str):
    """
    Get the status and remaining balance of a token.

    Args:
        token_id: The agentic token ID

    Returns:
        Token status and balance information
    """
    try:
        r = requests.get(f"{GATEWAY}/token/{token_id}")

        return r.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
