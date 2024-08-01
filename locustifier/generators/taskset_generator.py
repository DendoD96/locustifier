import textwrap
from typing import List

from black import FileMode, format_str
from locustifier.generators.task_generator import generate_locust_task_code
from locustifier.models.locust_taskset import LocustTaskSet


TASK_FILE_BASE_STRUCTURE = """
from {requests_module} import {requests_file}
from locust import task, {taskset_type}


class {task_set_name}({taskset_type}):
{task_list}
"""


def generate_taskset(
    taskset: LocustTaskSet,
    requests_module: str,
    requests_file: str,
    taskset_name: str,
) -> str:
    """
    Generate a Locust TaskSet code.

    Args:
        taskset (LocustTaskSet): The Locust TaskSet to be generated.
        requests_module (str): The name of the module containing the request\
              functions.
        requests_file (str): The name of the file containing the request\
              functions.
        taskset_name (str): The name of the generated TaskSet class.

    Returns:
        str: The generated Locust TaskSet code.
    """
    tasks: List[str] = [
        generate_locust_task_code(task, requests_file)
        for task in taskset.tasks
    ]
    return format_str(
        TASK_FILE_BASE_STRUCTURE.format(
            task_set_name=taskset_name,
            requests_module=requests_module,
            requests_file=requests_file,
            task_list=textwrap.indent("\n".join(tasks), "    "),
            taskset_type="SequentialTaskSet" if taskset.is_sequential
            else "TaskSet"
        ),
        mode=FileMode(),
    )
