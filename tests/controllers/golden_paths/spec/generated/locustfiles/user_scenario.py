from locust import FastHttpUser, between
from generated.locustfiles.tasks.user_scenario_tasks import UserScenarioTasks


class UserScenario(FastHttpUser):
    host = "http://localhost:8080"
    tasks = [UserScenarioTasks]
    wait_time = between(2, 5)
