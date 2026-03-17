const express = require("express");
const fetch = require("node-fetch");
const cors = require("cors");
const bodyParser = require("body-parser");

const app = express();

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

// Configuration
const GATEWAY_URL = process.env.GATEWAY_URL || "http://localhost:8000";

// Routes
app.get("/health", (req, res) => {
    res.json({ status: "ok" });
});

app.post("/agent-checkout", async (req, res) => {
    try {
        const { token, items, merchantId } = req.body;

        // Validate input
        if (!token || !items || !Array.isArray(items)) {
            return res.status(400).json({
                status: "error",
                message: "Invalid request: token and items required"
            });
        }

        // Call gateway
        const response = await fetch(`${GATEWAY_URL}/checkout`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                merchant: "shopify",
                token: token,
                items: items,
                merchant_id: merchantId
            })
        });

        const data = await response.json();

        res.json(data);
    } catch (error) {
        console.error("Checkout error:", error);
        res.status(500).json({
            status: "error",
            message: "Checkout processing failed"
        });
    }
});

app.post("/create-token", async (req, res) => {
    try {
        const { user, amount } = req.body;

        if (!user || !amount) {
            return res.status(400).json({
                status: "error",
                message: "user and amount are required"
            });
        }

        const response = await fetch(`${GATEWAY_URL}/token`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                user: user,
                amount: amount
            })
        });

        const data = await response.json();

        res.json(data);
    } catch (error) {
        console.error("Token creation error:", error);
        res.status(500).json({
            status: "error",
            message: "Token creation failed"
        });
    }
});

app.get("/token-status/:tokenId", async (req, res) => {
    try {
        const { tokenId } = req.params;

        const response = await fetch(`${GATEWAY_URL}/token/${tokenId}`);
        const data = await response.json();

        res.json(data);
    } catch (error) {
        console.error("Token status error:", error);
        res.status(500).json({
            status: "error",
            message: "Failed to get token status"
        });
    }
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({
        status: "error",
        message: "Internal server error"
    });
});

// Start server
const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
    console.log(`Shopify Agentic Commerce app running on port ${PORT}`);
});
