from locust import HttpUser, task, between

class FastApiUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def hello_world(self):
        self.client.get("/")

    @task
    def exception(self):
        self.client.get("/exception")

    @task
    def exclude(self):
        self.client.get("/exclude")

