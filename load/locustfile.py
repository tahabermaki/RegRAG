"""Test de charge (phase 6). Usage : locust -f load/locustfile.py --host http://localhost:8000"""

from locust import HttpUser, between, task


class Auditor(HttpUser):
    wait_time = between(1, 3)

    @task(1)
    def health(self):
        self.client.get("/health")

    # Phase 2 : décommenter quand /ask fonctionne
    # @task(5)
    # def ask(self):
    #     self.client.post("/ask", json={"question": "Que dit l'article 50 de l'AI Act ?"})
