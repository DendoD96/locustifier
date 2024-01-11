import textwrap
from black import FileMode, format_str

from sample.models.locust_task import LocustTask


REQUEST_CODE_TEMPLATE = """
def {function_name}(client):
    client.request(method='{method}', url='{url}', {optional_parameters})
"""


def __get_request_path(path_template, path_params) -> str:
    if path_params:
        return path_template.format(
            **{param.name: param.value for param in path_params}
        )
    return path_template


def __get_optional_parameter(headers, query_params, req_body) -> dict:
    optional_parameters = ""
    if headers:
        optional_parameters += f"headers={headers}, "
    if query_params:
        optional_parameters += f"params={query_params}, "
    if req_body:
        body_parameter_dict = {
            param.name: param.generate_value() for param in req_body
        }
        optional_parameters += f"json={body_parameter_dict}"
    return optional_parameters


def generate_request_code(task: LocustTask) -> str:
    """
    Generate locust request code for a given task.

    Args:
        task (LocustTask): The locust task for which \
            to generate the request code.

    Returns:
        str: The generated locust request code.
    """
    return format_str(
        textwrap.dedent(
            REQUEST_CODE_TEMPLATE.format(
                function_name=task.name,
                method=task.method,
                url=__get_request_path(
                    path_template=task.path, path_params=task.path_params
                ),
                optional_parameters=__get_optional_parameter(
                    headers=task.headers,
                    query_params=task.query_params,
                    req_body=task.req_body,
                ),
            )
        ),
        mode=FileMode(),
    )
