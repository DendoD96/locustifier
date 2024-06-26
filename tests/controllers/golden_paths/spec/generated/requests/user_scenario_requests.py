import inspect
from generated.requests.utils import generate_value


def get_user(client):
    client.request(
        name=inspect.currentframe().f_code.co_name,
        method="GET",
        url="/users/0326dce2-b212-427c-aa18-811648fb6594",
    )


def get_users(client):
    client.request(
        name=inspect.currentframe().f_code.co_name,
        method="GET",
        url="/users",
    )


def add_user(client):
    client.request(
        name=inspect.currentframe().f_code.co_name,
        method="POST",
        url="/users",
        json={
            "name": generate_value("str", None, 10, "name_nonbinary"),
            "lastname": generate_value("str", None, 10, "last_name_nonbinary"),
            "email": generate_value("str", None, 10, "email"),
            "id": generate_value("uuid", None, 10, None),
        },
    )
