from flask import Flask, jsonify

app = Flask(__name__)

products = {
    1: {'id': 1, 'name': 'Awesome T-Shirt', 'price': 20},
    2: {'id': 2, 'name': 'Cool Jeans', 'price': 50},
    3: {'id': 3, 'name': 'Stylish Hat', 'price': 15},
}

@app.route('/product/<int:product_id>')
def get_product(product_id):
    product = products.get(product_id)
    if product:
        return jsonify(product)
    else:
        return jsonify({'error': 'Product not found'}), 404

@app.route('/products')
def get_products():
    return jsonify(list(products.values()))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=False)