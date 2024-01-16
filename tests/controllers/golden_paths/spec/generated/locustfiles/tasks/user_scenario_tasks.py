from generated.requests import user_scenario_requests
from locust import task, TaskSet


class UserScenarioTasks(TaskSet):
    @task(1)
    def get_user(self):
        user_scenario_requests.get_user(self.client)

    @task(1)
    def get_users(self):
        user_scenario_requests.get_users(self.client)

    @task(1)
    def add_user(self):
        user_scenario_requests.add_user(self.client)
