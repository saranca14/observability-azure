from locust import HttpUser, task, between
import json

class ExternalAPIUser(HttpUser):
    wait_time = between(1, 3)  # Wait time between tasks (1-3 seconds)

    product_id = 1  # Hardcoded product_id for testing
    quantity = 1    # Hardcoded quantity for testing

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
        """POST /order with a hardcoded product ID and quantity"""
        order_data = {
            "product_id": self.product_id,  # Hardcoded product ID
            "quantity": self.quantity       # Hardcoded quantity
        }

        # Log the order data to verify it's being sent correctly
        print(f"Sending order data: {order_data}")

        # Send POST request with JSON body to the /order endpoint
        response = self.client.post("/order", json=order_data)

        # Check the response status and log the result
        if response.status_code == 200:
            try:
                # Outputting the entire JSON response
                print(f"POST /order success for product {self.product_id}:", response.json())
                # If you want to further analyze or assert the response, you can access the keys like:
                # print(response.json()['message'])
                # print(response.json()['product']['name'])
            except ValueError:
                print(f"POST /order success for product {self.product_id} but response is not JSON")
        else:
            print(f"POST /order failed for product {self.product_id}: {response.status_code} - {response.text}")

    def on_start(self):
        print("Starting test on external endpoint")
