from flask import Flask, render_template, request, jsonify
import requests
import os

print("---- Environment Variable Check ----")
endpoint = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT")
protocol = os.environ.get("OTEL_EXPORTER_OTLP_PROTOCOL")
service_name = os.environ.get("OTEL_SERVICE_NAME")

print(f"OTEL_EXPORTER_OTLP_ENDPOINT: {endpoint}")
print(f"OTEL_EXPORTER_OTLP_PROTOCOL: {protocol}")
print(f"OTEL_SERVICE_NAME: {service_name}")
print("-----------------------------------")

app = Flask(__name__)

ORDERS_SERVICE_URL = os.environ.get("ORDERS_SERVICE_URL", "http://localhost:5000")
PRODUCTS_SERVICE_URL = os.environ.get("PRODUCTS_SERVICE_URL", "http://localhost:5001")

@app.route('/')
def index():
    try:
        # Fetch all products for display
        products_response = requests.get(f"{PRODUCTS_SERVICE_URL}/products")
        products_response.raise_for_status()
        products = products_response.json()
    except requests.exceptions.RequestException as e:
        return f"Error fetching products: {e}", 500

    return render_template('index.html', products=products)

@app.route('/order', methods=['POST'])
def place_order():
    product_id = request.form.get('product_id')
    if not product_id:
        return jsonify({'error': 'Missing product_id'}), 400

    try:
        order_response = requests.post(f"{ORDERS_SERVICE_URL}/order", json={'product_id': int(product_id)})
        order_response.raise_for_status()
        order_result = order_response.json()
        return jsonify(order_result), 200
    except requests.exceptions.RequestException as e:
         return jsonify({'error': f'Error placing order: {e}'}), 500


@app.route('/products')
def list_products():
    try:
        products_response = requests.get(f"{PRODUCTS_SERVICE_URL}/products")
        products_response.raise_for_status()
        return jsonify(products_response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)