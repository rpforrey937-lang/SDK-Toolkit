<?php

class WC_Gateway_Agentic extends WC_Payment_Gateway {

    public function __construct() {
        $this->id = 'agentic';
        $this->method_title = 'Agentic Pay';
        $this->method_description = 'Accept AI agent autonomous payments using agentic tokens';

        $this->has_fields = true;
        $this->supports = array(
            'products',
            'refunds'
        );

        $this->init_form_fields();
        $this->init_settings();

        $this->title = $this->get_option('title');
        $this->description = $this->get_option('description');
        $this->gateway_url = $this->get_option('gateway_url', 'http://localhost:8000');

        // Save settings
        add_action('woocommerce_update_options_payment_gateways_' . $this->id, array($this, 'process_admin_options'));
    }

    public function init_form_fields() {
        $this->form_fields = array(
            'enabled' => array(
                'title' => 'Enable/Disable',
                'label' => 'Enable Agentic Pay',
                'type' => 'checkbox',
                'description' => '',
                'default' => 'no'
            ),
            'title' => array(
                'title' => 'Title',
                'type' => 'text',
                'description' => 'This controls the title which the user sees during checkout.',
                'default' => 'Agentic Pay',
                'desc_tip' => true,
            ),
            'description' => array(
                'title' => 'Description',
                'type' => 'textarea',
                'description' => 'This controls the description which the user sees during checkout.',
                'default' => 'Pay using your AI agent payment token',
                'desc_tip' => true,
            ),
            'gateway_url' => array(
                'title' => 'Gateway URL',
                'type' => 'text',
                'description' => 'URL of the Agentic Commerce Gateway',
                'default' => 'http://localhost:8000',
                'desc_tip' => true,
            ),
        );
    }

    public function payment_fields() {
        echo '<fieldset id="wc-' . esc_attr($this->id) . '-cc-form" class="wc-credit-card-form wc-payment-form">';
        
        if ($this->description) {
            echo wpautop(wp_kses_post($this->description));
        }

        echo '<p class="form-row form-row-wide">';
        echo '<label for="agentic_token">' . esc_html('Agentic Token') . ' <span class="required">*</span></label>';
        echo '<input type="text" id="agentic_token" name="agentic_token" placeholder="tok_..." required />';
        echo '</p>';

        echo '<div class="clear"></div>';
        echo '</fieldset>';
    }

    public function validate_fields() {
        if (empty($_POST['agentic_token'])) {
            wc_add_notice('Agentic Token is required', 'error');
            return false;
        }
        return true;
    }

    public function process_payment($order_id) {
        $order = wc_get_order($order_id);

        $token = sanitize_text_field($_POST['agentic_token']);

        // Prepare checkout data
        $items = array();
        foreach ($order->get_items() as $item) {
            $items[] = array(
                'product' => $item->get_name(),
                'price' => (float) $item->get_total()
            );
        }

        // Call gateway
        $response = wp_remote_post(
            $this->gateway_url . '/checkout',
            array(
                'method' => 'POST',
                'timeout' => 45,
                'redirection' => 5,
                'httpversion' => '1.0',
                'blocking' => true,
                'headers' => array(
                    'Content-Type' => 'application/json'
                ),
                'body' => json_encode(array(
                    'merchant' => 'woocommerce',
                    'token' => $token,
                    'items' => $items,
                    'total' => (float) $order->get_total()
                ))
            )
        );

        if (is_wp_error($response)) {
            wc_add_notice('Payment processing error: ' . $response->get_error_message(), 'error');
            return array(
                'result' => 'fail',
                'redirect' => ''
            );
        }

        $body = json_decode(wp_remote_retrieve_body($response), true);

        if ($body && $body['status'] === 'success') {
            // Mark order as processing
            $order->payment_complete($body['order_id']);
            $order->add_order_note('Agentic Payment Token: ' . $token);

            // Remove cart
            WC()->cart->empty_cart();

            return array(
                'result' => 'success',
                'redirect' => $this->get_return_url($order)
            );
        } else {
            wc_add_notice('Payment failed with agentic gateway', 'error');
            return array(
                'result' => 'fail',
                'redirect' => ''
            );
        }
    }

    public function process_refund($order_id, $amount = null, $reason = '') {
        // Refund logic would go here
        return true;
    }
}
