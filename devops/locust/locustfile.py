from locust import HttpUser, task, between
import random
import os

class ExternalAPIUser(HttpUser):
    wait_time = between(1, 3)

    # Load product IDs from environment or simulate them
    product_ids = list(range(1, 6))  # Simulating 5 products with IDs from 1 to 5

    @task
    def hit_get_root(self):
        """GET /"""
        response = self.client.get("/")
        if response.status_code == 200:
            try:
                print("GET / Success:", response.json())
            except ValueError:
                print("GET / Success but response is not JSON")
        else:
            print(f"GET / Failed: {response.status_code}")

    @task
    def create_order(self):
        """POST /order with a random product ID"""
        if not self.product_ids:
            print("No product IDs available. Skipping order placement.")
            return

        product_id = random.choice(self.product_ids)  # Pick a random product
        order_data = {
            "product_id": product_id,
            "quantity": 1
        }
        print(f"Sending order data: {order_data}")  # Log the order data to check if product_id is set correctly

        response = self.client.post("/order", json=order_data)

        if response.status_code == 200:
            try:
                print(f"POST /order success for product {product_id}:", response.json())
            except ValueError:
                print(f"POST /order success for product {product_id} but response is not JSON")
        else:
            print(f"POST /order failed for product {product_id}: {response.status_code} - {response.text}")

    def on_start(self):
        print("Starting test on external endpoint")
