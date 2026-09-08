import pytest
from pydantic_ai import UnexpectedModelBehavior, models
from pydantic_ai.models.test import TestModel
from agent import agent, MyDeps
from mock_data import CUSTOMERS, KNOWLEDGE_BASE
from models import TicketClassification

# Block real LLM calls — if TestModel isn't wired right, this catches it
models.ALLOW_MODEL_REQUESTS = False

pytestmark = pytest.mark.anyio


def make_deps(ticket_text: str = "") -> MyDeps:
    return MyDeps(
        customers=CUSTOMERS,
        knowledge_base=KNOWLEDGE_BASE,
        ticket_text=ticket_text,
    )


async def test_returns_valid_classification():
    """TestModel should return data that passes our Pydantic model validation."""
    with agent.override(model=TestModel()):
        result = await agent.run(
            "I am not able to login, account C-1234",
            deps=make_deps("I am not able to login, account C-1234"),
        )
    output = result.output
    assert output.category in ["account", "billing", "technical", "general"]
    assert 1 <= output.priority <= 5
    assert len(output.summary) <= 100
    assert len(output.suggested_action) > 0


async def test_tools_are_called():
    """TestModel calls all registered tools by default — verify they don't crash."""
    with agent.override(model=TestModel()):
        result = await agent.run(
            "I need help with billing, account C-1001",
            deps=make_deps("I need help with billing, account C-1001"),
        )
    # If we get here without an exception, tools ran fine
    assert result.output is not None


async def test_output_validator_rejects_low_priority_on_urgent_ticket():
    """Output validator should accept urgent tickets with priority >= 3."""
    urgent_ticket = "URGENT: Production is down and we are losing data"

    custom_output = TicketClassification(
        category="technical",
        priority=4,
        summary="Production outage",
        suggested_action="Escalate immediately",
    )

    with agent.override(model=TestModel(custom_output_args=custom_output)):
        result = await agent.run(
            urgent_ticket,
            deps=make_deps(urgent_ticket),
        )
    assert result.output.priority >= 3


async def test_output_validator_rejects_priority_1_on_urgent_ticket():
    """Validator should reject low priority when urgent keywords are present."""
    urgent_ticket = "URGENT: Production is down"

    bad_output = TicketClassification(
        category="technical",
        priority=1,
        summary="Some issue",
        suggested_action="Do something",
    )

    with pytest.raises(UnexpectedModelBehavior):
        with agent.override(model=TestModel(custom_output_args=bad_output)):
            await agent.run(
                urgent_ticket,
                deps=make_deps(urgent_ticket),
            )


async def test_priority_validator_range():
    """Pydantic should reject priority outside 1-5."""
    from pydantic import ValidationError
    from models import TicketClassification

    with pytest.raises(ValidationError):
        TicketClassification(
            category="billing",
            priority=0,
            summary="test",
            suggested_action="test",
        )

    with pytest.raises(ValidationError):
        TicketClassification(
            category="billing",
            priority=6,
            summary="test",
            suggested_action="test",
        )
