from fastapi import FastAPI
from pydantic import BaseModel
import uuid

app = FastAPI(title="Agentic Commerce Gateway")

# In-memory token store (replace with database in production)
TOKENS = {}


class TokenRequest(BaseModel):
    user: str
    amount: float


class CheckoutRequest(BaseModel):
    merchant: str
    token: str
    items: list


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/token")
def create_token(data: TokenRequest):
    """
    Create a new agentic payment token.

    Args:
        data: TokenRequest with user and amount

    Returns:
        Token data with token string and limit
    """
    token = "tok_" + str(uuid.uuid4())

    TOKENS[token] = {
        "user": data.user,
        "amount": data.amount,
        "used": 0
    }

    return {
        "token": token,
        "limit": data.amount,
        "user": data.user
    }


@app.post("/checkout")
def checkout(data: CheckoutRequest):
    """
    Process a checkout with an agentic token.

    Args:
        data: CheckoutRequest with merchant, token, and items

    Returns:
        Checkout status and order ID
    """
    token = data.token

    if token not in TOKENS:
        return {"status": "error", "message": "invalid token"}

    order_id = str(uuid.uuid4())

    # Update token usage
    TOKENS[token]["used"] += sum(item.get("price", 0) for item in data.items)

    return {
        "status": "success",
        "order_id": order_id,
        "merchant": data.merchant,
        "items": data.items
    }


@app.get("/token/{token_id}")
def get_token(token_id: str):
    """Get token details and remaining balance."""
    if token_id not in TOKENS:
        return {"status": "error", "message": "token not found"}

    token_data = TOKENS[token_id]
    remaining = token_data["amount"] - token_data["used"]

    return {
        "token": token_id,
        "user": token_data["user"],
        "limit": token_data["amount"],
        "used": token_data["used"],
        "remaining": remaining
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
