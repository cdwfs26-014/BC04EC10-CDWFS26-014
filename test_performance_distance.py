"""Test de performance : charge Locust sur un conteneur testcontainers.

Construit l'image depuis le Dockerfile, lance le conteneur, puis applique une
charge Locust. Necessite Docker (testcontainers).
"""

import gevent
from locust import HttpUser, task
from locust.env import Environment
from locust.stats import stats_printer
from testcontainers.core.container import DockerContainer
from testcontainers.core.image import DockerImage
from testcontainers.core.waiting_utils import wait_for_logs


class MyDistanceHttp(HttpUser):
    @task
    def my_distance(self):
        self.client.get("/")
        self.client.post("/api/distance", json={"start_point": "2,5", "end_point": "1,6"})


def test_performance():
    with DockerImage(path=".", tag="testcontainermydistance:latest") as image:
        with DockerContainer(str(image), ports=[5000]) as container:
            wait_for_logs(container, "Running on http")
            exposed_port = container.get_exposed_port(5000)
            MyDistanceHttp.host = f"http://localhost:{exposed_port}/"
            env = Environment(user_classes=[MyDistanceHttp])
            gevent.spawn(stats_printer(env.stats))
            runner = env.create_local_runner()
            runner.start(5, 0.25)
            gevent.spawn_later(60, runner.quit)
            runner.greenlet.join()
