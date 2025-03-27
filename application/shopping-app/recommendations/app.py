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

recommendations = {
    1: [{'id': 2, 'name': 'Cool Jeans'}, {'id': 3, 'name': 'Stylish Hat'}],
    2: [{'id': 1, 'name': 'Awesome T-Shirt'}],
    3: [{'id': 1, 'name': 'Awesome T-Shirt'}],
}

@app.route('/recommendations/<int:product_id>')
def get_recommendations(product_id):
    logging.info(f"Fetching recommendations for product ID: {product_id}")
    recommendation = recommendations.get(product_id)
    if recommendation:
        logging.info(f"Recommendations found: {recommendation}")
        return jsonify(recommendation)
    else:
        logging.info(f"No recommendations found for product ID: {product_id}")
        return jsonify([]) # Return empty list if no recommendations

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=False)