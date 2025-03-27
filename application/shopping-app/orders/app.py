from flask import Flask, request, jsonify
import requests
import os
import logging

# Configure logging
logging.basicConfig(
    format='%(asctime)s %(levelname)s [%(name)s] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s] - %(message)s',
    level=logging.INFO,
)
log = logging.getLogger('werkzeug')
log.disabled = True

app = Flask(__name__)

PRODUCTS_SERVICE_URL = os.environ.get("PRODUCTS_SERVICE_URL", "http://localhost:5001")
RECOMMENDATIONS_SERVICE_URL = os.environ.get("RECOMMENDATIONS_SERVICE_URL", "http://localhost:5002")
PAYMENT_SERVICE_URL = os.environ.get("PAYMENT_SERVICE_URL", "http://localhost:5003")

@app.route('/order', methods=['POST'])
def place_order():
    order_data = request.json
    product_id = order_data.get('product_id')
    if not product_id:
        logging.warning("Missing product_id")
        return jsonify({'error': 'Missing product_id'}), 400

    # Get product details
    try:
        product_response = requests.get(f"{PRODUCTS_SERVICE_URL}/product/{product_id}")
        product_response.raise_for_status()
        product = product_response.json()
        logging.info(f"Product details fetched: {product}")
    except requests.exceptions.RequestException as e:
        logging.error(f'Error fetching product: {e}')
        return jsonify({'error': f'Error fetching product: {e}'}), 500

    # Get recommendations
    try:
        recommendations_response = requests.get(f"{RECOMMENDATIONS_SERVICE_URL}/recommendations/{product_id}")
        recommendations_response.raise_for_status()
        recommendations = recommendations_response.json()
        logging.info(f"Recommendations fetched: {recommendations}")
    except requests.exceptions.RequestException as e:
        logging.error(f'Error fetching recommendations: {e}')
        return jsonify({'error': f'Error fetching recommendations: {e}'}), 500

    # Process payment
    try:
        payment_response = requests.post(f"{PAYMENT_SERVICE_URL}/payment", json=order_data)
        payment_response.raise_for_status()
        payment = payment_response.json()
        logging.info(f"Payment processed: {payment}")
    except requests.exceptions.RequestException as e:
        logging.error(f'Error processing payment: {e}')
        return jsonify({'error': f'Error processing payment: {e}'}), 500

    logging.info("Order placed successfully")
    return jsonify({'message': 'Order placed!', 'product': product, 'recommendations': recommendations, 'payment': payment}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)