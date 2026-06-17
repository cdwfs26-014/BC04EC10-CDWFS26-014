from locust import HttpUser, task


class MyDistance(HttpUser):
    @task
    def my_distance(self):
        self.client.get("/")
        self.client.post("/api/distance", json={"start_point": "2,5", "end_point": "1,6"})
