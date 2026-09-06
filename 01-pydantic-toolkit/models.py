import re
from typing import Literal
from pydantic import BaseModel, Field, field_validator

class ToolParameter(BaseModel):
    name: str
    param_type: Literal["string", "integer", "boolean", "number"]
    description: str = Field(
        min_length=5,
        max_length=400
    )
    required: bool = True

class Tool(BaseModel):
    name: str
    description: str = Field(
        min_length=5,
        max_length=400
    )
    parameters: list[ToolParameter]

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if not re.fullmatch(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)*", value):
            raise ValueError("name must be snake_case")
        return value

    @field_validator("parameters")
    @classmethod
    def validate_parameter(cls, value):
        if len(value) == 0:
            raise ValueError("parameters cannot be empty")
        return value


if __name__ == "__main__":
    tool = Tool(
        name="create_ticket",
        description="Creates a support ticket",
        parameters=[
            ToolParameter(name="title", param_type="string", description="Title of the ticket", required=True),
            ToolParameter(name="priority", param_type="integer", description="Priority from 1 to 5", required=True),
            ToolParameter(name="description", param_type="string", description="Detailed description", required=False),
        ]
    )
    # print(tool)
    print(tool.model_dump_json(indent=2))
    # print(Tool.model_json_schema())