from typing import Optional, Literal
from pydantic import BaseModel, Field, validator
from sample.utils import fake

BASIC_PROVIDER = {
    "int": "random_int",
    "float": "pyfloat",
    "bool": "pybool",
    "str": "word",
}
MAX_LIST_ELEM = 900


class BaseParameter(BaseModel):
    type: Literal["int", "float", "bool", "str", "list"]
    count: int = Field(default=10, lt=900)
    items: Optional["BaseParameter"] = None

    @validator("count", "items", pre=True, always=True)
    def check_conditional_field(cls, value, values):
        type = values.get("type")

        if type == "list" and value is None:
            raise ValueError("{{value}} is required when type is a list")

        return value

    # NOTE: On parsing we should check the recursion limit and if the provider
    #       is suitable for choosen type
    def generate_value(self):
        def recursive_generate_value(
            parameter: FakeBodyParameter | BaseParameter,
        ):
            if parameter.type in ["int", "float", "bool", "str"]:
                generator = getattr(
                    fake,
                    self.provider
                    if self.provider
                    else BASIC_PROVIDER[self.type],
                    None,
                )
                return generator()

            return [
                recursive_generate_value(parameter.items)
                for _ in range(parameter.count)
            ]

        return recursive_generate_value(self)


class FakeBodyParameter(BaseParameter):
    name: str
    provider: Optional[str] = None
