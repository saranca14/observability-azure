from locust import HttpUser, task, between

class ExternalAPIUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def hit_get_root(self):
        """GET /"""
        response = self.client.get("/")
        if response.status_code == 200:
            print("GET / Success:", response.json())
        else:
            print("GET / Failed:", response.status_code)

    @task
    def create_order(self):
        """POST /order"""
        order_data = {
            "product_id": 123,
            "quantity": 1
        }
        response = self.client.post("/order", json=order_data)
        if response.status_code == 201:
            print("POST /order Success:", response.json())
        else:
            print("POST /order Failed:", response.status_code)

    def on_start(self):
        print("Starting test on external endpoint")


