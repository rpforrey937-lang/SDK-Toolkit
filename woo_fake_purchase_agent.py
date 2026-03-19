#!/usr/bin/env python3
"""Sample agent: make a fake WooCommerce purchase using the Agentic SDK.

This script demonstrates how an AI agent can create a payment token and
complete a checkout on a sample WooCommerce store using the Agentic Commerce
Gateway.

The purchase is "fake" in the sense that the gateway is a lightweight demo
implementation (see `gateway/app.py`) and does not integrate with a real
payment processor.

Requirements:
  - Gateway running (default: http://localhost:8000)
  - Optional: A WooCommerce store with the Agentic Pay plugin configured to
    point at the same gateway URL.

Example:
  python woo_fake_purchase_agent.py \
    --api-key demo-key-12345 \
    --gateway-url http://localhost:8000 \
    --user demo-user \
    --amount 49.99 \
    --item "T-shirt:49.99"
"""

import argparse
import json
import os
import sys

# Ensure the SDK package is importable when running from the repository root.
sys.path.insert(0, "sdk-python")

from agentic_sdk import AgentClient


def parse_item(item_str):
    """Parse an item declaration of the form 'name:price[:quantity]'."""
    parts = item_str.split(":")
    if len(parts) < 2:
        raise ValueError("Item must be in the format 'name:price' or 'name:price:quantity'")

    product = parts[0].strip()
    try:
        price = float(parts[1])
    except ValueError:
        raise ValueError("Price must be a number")

    quantity = 1
    if len(parts) >= 3 and parts[2].strip():
        try:
            quantity = int(parts[2])
        except ValueError:
            raise ValueError("Quantity must be an integer")

    return {"product": product, "price": price, "quantity": quantity}


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Agentic SDK sample agent that makes a fake WooCommerce purchase."
    )

    parser.add_argument(
        "--api-key",
        default="demo-key-12345",
        help="API key for the Agentic Gateway (default: demo-key-12345)",
    )
    parser.add_argument(
        "--gateway-url",
        default="http://localhost:8000",
        help="Agentic Gateway base URL (default: http://localhost:8000)",
    )
    parser.add_argument(
        "--merchant",
        default="woocommerce",
        help="Merchant identifier (default: woocommerce)",
    )
    parser.add_argument(
        "--user",
        default="agentic-demo",
        help="User/agent identifier (default: agentic-demo)",
    )
    parser.add_argument(
        "--amount",
        type=float,
        default=50.0,
        help="Token amount limit (default: 50.0)",
    )
    parser.add_argument(
        "--item",
        action="append",
        default=["Sample Product:50.00"],
        help=(
            "Item to purchase in the format 'name:price[:quantity]'. "
            "Can be specified multiple times."
        ),
    )

    args = parser.parse_args(argv)

    # Ensure the SDK points at the gateway URL provided.
    os.environ["AGENTIC_API_URL"] = args.gateway_url

    print("\n== Agentic WooCommerce Fake Purchase Agent ==\n")
    print(f"Gateway URL: {args.gateway_url}")
    print(f"Merchant:   {args.merchant}")
    print(f"User:       {args.user}")
    print(f"Token limit: ${args.amount:.2f}\n")

    agent = AgentClient(api_key=args.api_key)

    # Create token
    token_resp = agent.create_token(user=args.user, amount=args.amount)
    token = token_resp.get("token")
    if not token:
        print("ERROR: Failed to create token. Response:")
        print(json.dumps(token_resp, indent=2))
        sys.exit(1)

    print("[1] Created token")
    print(f"    Token: {token}")

    # Build items list
    items = []
    for item_str in args.item:
        try:
            items.append(parse_item(item_str))
        except ValueError as e:
            print(f"ERROR: Invalid item '{item_str}': {e}")
            sys.exit(1)

    print("\n[2] Items:")
    for it in items:
        print(f"    - {it['product']} (qty={it.get('quantity', 1)}): ${it['price']:.2f}")

    # Checkout
    print("\n[3] Processing checkout...")
    order_resp = agent.checkout(merchant=args.merchant, token=token, items=items)

    if order_resp.get("status") != "success":
        print("ERROR: Checkout failed")
        print(json.dumps(order_resp, indent=2))
        sys.exit(1)

    print("\n[4] Checkout successful")
    print(f"    Order ID: {order_resp.get('order_id')}")
    print(f"    Merchant: {order_resp.get('merchant')}")
    print(f"    Status:   {order_resp.get('status')}\n")

    print("Done. You can now use the token in a WooCommerce checkout using the Agentic Pay plugin.")


if __name__ == "__main__":
    main()
