from flask import Flask, request, jsonify
import random
import logging

# Configure logging
logging.basicConfig(
    format='%(asctime)s %(levelname)s [%(name)s] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s] - %(message)s',
    level=logging.INFO,
)
log = logging.getLogger('werkzeug')
log.disabled = True

app = Flask(__name__)

@app.route('/payment', methods=['POST'])
def process_payment():
    # Simulate payment processing (success/failure)
    order_data = request.json
    logging.info(f"Processing payment for order: {order_data}") #log the request data

    success = random.choice([True, False])
    if success:
        message = 'Payment successful!'
        transaction_id = 'TXN12345'
        logging.info(f"{message}, transaction_id: {transaction_id}") #log success
        return jsonify({'message': message, 'transaction_id': transaction_id}), 200
    else:
        message = 'Payment failed!'
        logging.error(message) #log error
        return jsonify({'error': message}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5003, debug=False)