import textwrap
from black import FileMode, format_str

from sample.models.locust_task import LocustTask


LOCUST_TASK_CODE_TEMPLATE = """
@task({weight})
def {task_name}(self):
    {requests_file}.{task_name}(self.client)
"""


def generate_locust_task_code(task: LocustTask, requests_file: str) -> str:
    """
    Generate Locust task code.

    Args:
        task (LocustTask): The Locust task to be generated.
        requests_file (str): The name of the file containing the request \
            functions.

    Returns:
        str: The generated Locust task code.
    """
    return format_str(
        textwrap.dedent(
            LOCUST_TASK_CODE_TEMPLATE.format(
                requests_file=requests_file,
                weight=task.weight,
                task_name=task.name,
            )
        ),
        mode=FileMode(),
    )
