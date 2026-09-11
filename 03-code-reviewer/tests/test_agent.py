import pytest
from pydantic import ValidationError
from pydantic_ai import UnexpectedModelBehavior, models
from pydantic_ai.messages import ToolReturnPart
from pydantic_ai.models.test import TestModel
from agent import agent, check_naming_convention, number_lines
from mock_data import SAMPLE_FUNCTIONS
from models import CodeReview, Issue, Quality, Severity

# Block real LLM calls — if TestModel isn't wired right, this catches it
models.ALLOW_MODEL_REQUESTS = False

pytestmark = pytest.mark.anyio

MESSY_CODE = number_lines(SAMPLE_FUNCTIONS["messy"])


async def test_returns_valid_review():
    """TestModel fabricates output from the schema — it should validate into a CodeReview."""
    with agent.override(model=TestModel()):
        result = await agent.run(MESSY_CODE)
    output = result.output
    assert isinstance(output, CodeReview)
    assert isinstance(output.overall_quality, Quality)
    assert all(isinstance(issue.severity, Severity) for issue in output.issues)
    assert isinstance(output.summary, str)


async def test_naming_tool_is_called():
    """The agent should be able to call check_naming_convention and get its result back."""
    with agent.override(model=TestModel(call_tools=["check_naming_convention"])):
        result = await agent.run(MESSY_CODE)
    tool_returns = [
        part
        for message in result.all_messages()
        for part in message.parts
        if isinstance(part, ToolReturnPart)
        and part.tool_name == "check_naming_convention"
    ]
    assert len(tool_returns) == 1
    assert set(tool_returns[0].content) == {"passes", "reason"}


async def test_model_output_is_parsed_into_enums():
    """Raw JSON-style output from the model should be validated into typed enums."""
    raw_output = {
        "issues": [
            {
                "description": "Bare except swallows every error",
                "severity": "critical",
                "line_reference": "line 9",
            },
            {"description": "Missing docstring", "severity": "suggestion"},
        ],
        "overall_quality": "poor",
        "suggestions": ["Catch a specific exception instead of using bare except"],
        "summary": "Works for happy-path input but hides every failure.",
    }
    with agent.override(model=TestModel(custom_output_args=raw_output)):
        result = await agent.run(MESSY_CODE)
    output = result.output
    assert output.overall_quality is Quality.POOR
    assert output.issues[0].severity is Severity.CRITICAL
    assert output.issues[0].line_reference == "line 9"
    assert output.issues[1].line_reference is None


async def test_invalid_model_output_fails_the_run():
    """An out-of-schema quality value should be rejected, retried, and then fail the run."""
    bad_output = {
        "issues": [],
        "overall_quality": "excellent",
        "suggestions": [],
        "summary": "Looks great.",
    }
    with pytest.raises(UnexpectedModelBehavior):
        with agent.override(model=TestModel(custom_output_args=bad_output)):
            await agent.run(MESSY_CODE)


def test_severity_must_be_a_known_value():
    """Pydantic should reject severities outside the enum."""
    with pytest.raises(ValidationError):
        Issue(description="Something is off", severity="blocker")


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("calculate_average", True),
        ("_private_helper", True),
        ("__init__", True),
        ("getUserAge", False),
        ("CalculateAverage", False),
        ("get__name", False),
        ("2fast", False),
        ("class", False),
    ],
)
def test_check_naming_convention(name, expected):
    assert check_naming_convention(name)["passes"] is expected
