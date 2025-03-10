from flask import Flask, jsonify

app = Flask(__name__)

recommendations = {
    1: [{'id': 2, 'name': 'Cool Jeans'}, {'id': 3, 'name': 'Stylish Hat'}],
    2: [{'id': 1, 'name': 'Awesome T-Shirt'}],
    3: [{'id': 1, 'name': 'Awesome T-Shirt'}],
}
@app.route('/recommendations/<int:product_id>')
def get_recommendations(product_id):
    recommendation = recommendations.get(product_id)
    if recommendation:
        return jsonify(recommendation)
    return jsonify([]) # Return empty list if no recommendations


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)