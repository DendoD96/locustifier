import textwrap
from black import FileMode, format_str

from locustifier.models.locust_task import LocustTask
from locustifier.models.locust_taskset import LocustTaskSet
from locustifier.utils import string_to_snake_case


REQUEST_CODE_TEMPLATE = """
def {function_name}(client):
    client.request(name=inspect.currentframe().f_code.co_name, \
        method='{method}', url='{url}', {optional_parameters})
"""

REQUESTS_FILE_BASE_STRUCTURE = """
import inspect
from {request_utils_module} import generate_value

{requests_code}
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
        body_parameter_dict: str = ",".join(
            [
                (
                    f"'{param.name}': generate_value('"
                    f"{param.parameter_type}', "
                    f"{param.items}, {param.count}, "
                )
                + (f"'{param.provider}')" if param.provider else "None)")
                for param in req_body
            ]
        )
        optional_parameters += f"json={{{body_parameter_dict}}}"
    return optional_parameters


def __generate_request_code(task: LocustTask) -> str:
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
                function_name=string_to_snake_case(task.name),
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


def generate_requests_code(
    request_utils_module, taskset: LocustTaskSet
) -> str:
    """
    Generate requests code.

    This function takes the path to the request utilities module and a Locust
    task set as input. It generates and returns the requests code based
    for the provided task set.

    Parameters:
    - request_utils_module (str): The path to the request utilities module.
    - taskset (LocustTaskSet): The Locust task set containing tasks for which
      requests code should be generated.

    Returns:
    - str: The generated requests code as a string.
    """
    return format_str(
        textwrap.dedent(
            REQUESTS_FILE_BASE_STRUCTURE.format(
                request_utils_module=request_utils_module,
                requests_code="\n\n".join(
                    [__generate_request_code(task) for task in taskset.tasks]
                ),
            )
        ),
        mode=FileMode(),
    )
