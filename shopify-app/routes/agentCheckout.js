const fetch = require("node-fetch");

const GATEWAY_URL = process.env.GATEWAY_URL || "http://localhost:8000";

/**
 * Handle agent checkout requests from Shopify storefront
 */
async function handleAgentCheckout(req, res) {
    try {
        const { token, items, cartTotal, customerId } = req.body;

        // Validate required fields
        if (!token || !items || !Array.isArray(items)) {
            return res.status(400).json({
                success: false,
                error: "Missing required fields: token, items"
            });
        }

        // Call the agentic commerce gateway
        const response = await fetch(`${GATEWAY_URL}/checkout`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                merchant: "shopify",
                token: token,
                items: items,
                amount: cartTotal,
                customer_id: customerId
            })
        });

        if (!response.ok) {
            throw new Error(`Gateway returned status ${response.status}`);
        }

        const result = await response.json();

        // Return success result
        return res.json({
            success: true,
            orderId: result.order_id,
            status: result.status
        });
    } catch (error) {
        console.error("Agent checkout error:", error);

        return res.status(500).json({
            success: false,
            error: "Failed to process agent checkout",
            details: error.message
        });
    }
}

/**
 * Create a payment token for an agent
 */
async function createAgentToken(req, res) {
    try {
        const { userId, amount, expiryHours } = req.body;

        if (!userId || !amount) {
            return res.status(400).json({
                success: false,
                error: "Missing required fields: userId, amount"
            });
        }

        const response = await fetch(`${GATEWAY_URL}/token`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                user: userId,
                amount: amount
            })
        });

        if (!response.ok) {
            throw new Error(`Gateway returned status ${response.status}`);
        }

        const result = await response.json();

        return res.json({
            success: true,
            token: result.token,
            limit: result.limit
        });
    } catch (error) {
        console.error("Token creation error:", error);

        return res.status(500).json({
            success: false,
            error: "Failed to create agent token",
            details: error.message
        });
    }
}

module.exports = {
    handleAgentCheckout,
    createAgentToken
};
