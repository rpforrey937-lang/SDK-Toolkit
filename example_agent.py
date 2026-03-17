#!/usr/bin/env python3
"""
Example agent script demonstrating autonomous checkout using the Agentic SDK.
"""

import sys
sys.path.insert(0, 'sdk-python')

from agentic_sdk import AgentClient


def main():
    """Run an example autonomous checkout."""

    # Initialize the agent client
    agent = AgentClient(api_key="demo-key-12345")

    print("=" * 60)
    print("Agentic Commerce - Autonomous Checkout Example")
    print("=" * 60)
    print()

    # Step 1: Create a payment token
    print("[1] Creating payment token...")
    print("    User: customer123")
    print("    Amount: $80.00")

    token_response = agent.create_token(
        user="customer123",
        amount=80
    )

    print(f"    ✓ Token created: {token_response['token']}")
    print(f"    ✓ Limit: ${token_response['limit']}")
    print()

    token = token_response["token"]

    # Step 2: Create ordered items
    print("[2] Preparing order items...")

    items = [
        {
            "product": "running shoes",
            "price": 80,
            "quantity": 1
        }
    ]

    for item in items:
        print(f"    - {item['product']}: ${item['price']}")

    print()

    # Step 3: Process checkout
    print("[3] Processing checkout on WooCommerce...")
    print(f"    Token: {token}")
    print(f"    Merchant: woocommerce")

    order_response = agent.checkout(
        merchant="woocommerce",
        token=token,
        items=items
    )

    print(f"    ✓ Status: {order_response['status']}")
    print(f"    ✓ Order ID: {order_response['order_id']}")
    print()

    # Step 4: Example with Shopify
    print("[4] Creating second token for Shopify...")
    print("    User: customer456")
    print("    Amount: $150.00")

    token_response2 = agent.create_token(
        user="customer456",
        amount=150
    )

    token2 = token_response2["token"]

    print(f"    ✓ Token created: {token2}")
    print()

    # Step 5: Checkout on Shopify
    print("[5] Processing checkout on Shopify...")

    shopify_items = [
        {
            "product": "winter jacket",
            "price": 150,
            "quantity": 1
        }
    ]

    shopify_response = agent.checkout(
        merchant="shopify",
        token=token2,
        items=shopify_items
    )

    print(f"    ✓ Status: {shopify_response['status']}")
    print(f"    ✓ Order ID: {shopify_response['order_id']}")
    print()

    print("=" * 60)
    print("✓ Autonomous checkout successful!")
    print("=" * 60)


if __name__ == "__main__":
    main()
