<?php
/**
 * Plugin Name: Agentic Pay
 * Plugin URI: https://github.com/agentic-commerce/agentic-commerce-toolkit
 * Description: Accept AI agent autonomous payments using agentic tokens
 * Version: 1.0.0
 * Author: Agentic Commerce
 * License: GPL v2 or later
 * Text Domain: agentic-pay
 * Domain Path: /languages
 */

// Exit if accessed directly
if (!defined('ABSPATH')) {
    exit;
}

define('AGENTIC_PAY_PLUGIN_DIR', plugin_dir_path(__FILE__));

// Initialize the plugin
add_action('plugins_loaded', 'agentic_pay_init');

function agentic_pay_init() {
    if (!class_exists('WC_Payment_Gateway')) {
        return;
    }

    // Include the gateway class
    include AGENTIC_PAY_PLUGIN_DIR . 'class-agentic-gateway.php';

    // Register the payment method
    add_filter('woocommerce_payment_gateways', function($methods) {
        $methods[] = 'WC_Gateway_Agentic';
        return $methods;
    });
}

// Plugin activation hook
register_activation_hook(__FILE__, 'agentic_pay_activate');

function agentic_pay_activate() {
    // Placeholder for activation logic
}

// Plugin deactivation hook
register_deactivation_hook(__FILE__, 'agentic_pay_deactivate');

function agentic_pay_deactivate() {
    // Placeholder for deactivation logic
}
