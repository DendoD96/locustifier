from locust import HttpUser, between
from generated.locustfiles.tasks.user_scenario_tasks import UserScenarioTasks


class UserScenario(HttpUser):
    host = "http://localhost:8080"
    tasks = [UserScenarioTasks]
    wait_time = between(2, 5)
