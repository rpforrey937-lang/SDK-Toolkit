import requests
from .config import API_URL


class TokenManager:
    """Manages creation and handling of agentic payment tokens."""

    def create_token(self, user, amount):
        """
        Create a new payment token for an agent.

        Args:
            user: User or agent identifier
            amount: Token amount limit

        Returns:
            Token data with token string and limit
        """
        payload = {
            "user": user,
            "amount": amount
        }

        r = requests.post(f"{API_URL}/token", json=payload)

        return r.json()
