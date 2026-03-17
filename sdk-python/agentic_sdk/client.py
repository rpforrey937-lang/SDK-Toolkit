from .token_manager import TokenManager
from .checkout import Checkout


class AgentClient:
    """
    Main client for agents to interact with the Agentic Commerce Gateway.
    """

    def __init__(self, api_key):
        """
        Initialize the agent client.

        Args:
            api_key: API key for authentication with the gateway
        """
        self.api_key = api_key
        self.tokens = TokenManager()
        self.checkout_api = Checkout()

    def create_token(self, user, amount):
        """
        Create a new payment token.

        Args:
            user: User or agent identifier
            amount: Token amount limit

        Returns:
            Token data
        """
        return self.tokens.create_token(user, amount)

    def checkout(self, merchant, token, items):
        """
        Process a checkout with an agentic token.

        Args:
            merchant: Merchant identifier
            token: The agentic payment token
            items: List of items to purchase

        Returns:
            Order confirmation data
        """
        return self.checkout_api.create_order(
            merchant,
            token,
            items
        )
