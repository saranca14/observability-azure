from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route('/payment', methods=['POST'])
def process_payment():
    # Simulate payment processing (success/failure)
    order_data = request.json
    #in real scenario, payment will be processed, for now we will randomly return true or false
    success = random.choice([True, False])
    if success:
        return jsonify({'message': 'Payment successful!', 'transaction_id': 'TXN12345'}), 200
    else:
        return jsonify({'error': 'Payment failed!'}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5003, debug=False)