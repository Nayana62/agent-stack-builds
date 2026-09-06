from pydantic import ValidationError
import pytest
from models import Tool, ToolParameter


# --- Valid cases ---

def test_valid_tool_creation():
    tool = Tool(
        name="create_ticket",
        description="Creates a support ticket",
        parameters=[
            ToolParameter(name="title", param_type="string", description="Title of the ticket"),
        ]
    )
    assert tool.name == "create_ticket"
    assert tool.parameters[0].name == "title"
    assert tool.parameters[0].required == True  


def test_coercion():
    tool = Tool(
        name="create_ticket",
        description="Creates a support ticket",
        parameters=[
            ToolParameter(name="title", param_type="string", description="Title of the ticket", required=1),
        ]
    )
    assert tool.parameters[0].required == True  
    assert isinstance(tool.parameters[0].required, bool) 

# --- Invalid cases ---

def test_invalid_name_not_snake_case():
    with pytest.raises(ValidationError):
        Tool(name="Create Ticket", description="Creates a ticket", parameters=[
            ToolParameter(name="title", param_type="string", description="Title of the ticket"),
        ])

def test_invalid_param_type():
    with pytest.raises(ValidationError):
        Tool(name="Create Ticket", description="Creates a ticket", parameters=[
            ToolParameter(name="title", param_type="banana", description="Title of the ticket"),
        ])

def test_empty_parameters():
    with pytest.raises(ValidationError):
        Tool(name="Create Ticket", description="Creates a ticket", parameters=[])

def test_short_description():
    with pytest.raises(ValidationError):
        Tool(name="Create Ticket", description="test", parameters=[
            ToolParameter(name="title", param_type="string", description="Title of the ticket"),
        ])