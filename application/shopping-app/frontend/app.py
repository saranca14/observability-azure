from flask import Flask, render_template, request, jsonify
import requests
import os

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
    # Log the incoming request body for debugging purposes
    print("Received POST /order with body:", request.get_data())

    try:
        data = request.json
    except Exception as e:
        return jsonify({"error": f"Failed to parse JSON: {str(e)}"}), 400

    product_id = data.get('product_id')
    quantity = data.get('quantity')

    if not product_id or not quantity:
        return jsonify({'error': 'Missing product_id or quantity'}), 400

    # Process the order here...
    return jsonify({"status": "Order placed"}), 200

@app.route('/products')
def list_products():
    try:
        products_response = requests.get(f"{PRODUCTS_SERVICE_URL}/products")
        products_response.raise_for_status()
        return jsonify(products_response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=False)
