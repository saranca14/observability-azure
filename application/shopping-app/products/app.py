from flask import Flask, jsonify
import logging

# Configure logging
logging.basicConfig(
    format='%(asctime)s %(levelname)s [%(name)s] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s] - %(message)s',
    level=logging.INFO,
)
log = logging.getLogger('werkzeug')
log.disabled = True

app = Flask(__name__)

products = {
    1: {'id': 1, 'name': 'Awesome T-Shirt', 'price': 20},
    2: {'id': 2, 'name': 'Cool Jeans', 'price': 50},
    3: {'id': 3, 'name': 'Stylish Hat', 'price': 15},
}

@app.route('/product/<int:product_id>')
def get_product(product_id):
    logging.info(f"Fetching product with ID: {product_id}")
    product = products.get(product_id)
    if product:
        logging.info(f"Product found: {product}")
        return jsonify(product)
    else:
        logging.warning(f"Product with ID {product_id} not found")
        return jsonify({'error': 'Product not found'}), 404

@app.route('/products')
def get_products():
    logging.info("Fetching all products")
    logging.info(f"Products found: {list(products.values())}")
    return jsonify(list(products.values()))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=False)