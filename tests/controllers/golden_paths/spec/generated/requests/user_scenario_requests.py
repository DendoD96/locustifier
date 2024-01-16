from generated.requests.utils import generate_value


def get_user(client):
    client.request(
        method="GET",
        url="/users/0326dce2-b212-427c-aa18-811648fb6594",
    )


def get_users(client):
    client.request(
        method="GET",
        url="/users",
    )


def add_user(client):
    client.request(
        method="POST",
        url="/users",
        json={
            "name": generate_value("str", 10, "name_nonbinary"),
            "lastname": generate_value("str", 10, "last_name_nonbinary"),
            "email": generate_value("str", 10, "email"),
            "id": generate_value("uuid", 10, "None"),
        },
    )
