import requests
from .config import API_URL


class Checkout:
    """Handles checkout operations using agentic tokens."""

    def create_order(self, merchant, token, items):
        """
        Create a checkout order with an agentic token.

        Args:
            merchant: Merchant identifier (e.g., 'woocommerce', 'shopify')
            token: The agentic payment token
            items: List of items to purchase

        Returns:
            Order creation response with status and order_id
        """
        payload = {
            "merchant": merchant,
            "token": token,
            "items": items
        }

        r = requests.post(f"{API_URL}/checkout", json=payload)

        return r.json()
