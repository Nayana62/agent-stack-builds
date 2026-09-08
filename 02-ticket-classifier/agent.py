from dataclasses import dataclass, field

from pydantic import Field, BaseModel
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext, ModelRetry
from models import TicketClassification
from mock_data import CUSTOMERS, KNOWLEDGE_BASE

load_dotenv()


@dataclass
class MyDeps:
    customers: dict = field(default_factory=lambda: CUSTOMERS)
    knowledge_base: dict = field(default_factory=lambda: KNOWLEDGE_BASE)
    ticket_text: str = ""


agent = Agent(
    "google:gemini-3.6-flash",
    instructions="""You are a support ticket classifier. Your job is to read a customer support ticket and classify it.

When you receive a ticket:
1. Look for a customer/account ID (like C-1234). If you find one, use the lookup_customer tool to get their info.
2. Identify the main issue and use check_knowledge_base with a relevant keyword (like "login", "billing", "api", "export", "performance") to find related help articles.
3. Based on the ticket text, customer info, and knowledge base results, classify the ticket.

For priority, use this scale:
- 5: Critical — production is down, enterprise customer, data loss
- 4: High — customer is blocked from doing their work, time-sensitive
- 3: Medium — something is broken but there's a workaround
- 2: Low — general question, how-to, minor inconvenience
- 1: Minimal — feedback, feature request, no urgency

Consider the customer's plan when setting priority — an enterprise customer with a production issue is higher priority than a free-tier user with the same issue.

For suggested_action, be specific — say what the support team should actually do first, not generic advice.
""",
    output_type=TicketClassification,
    deps_type=MyDeps,
)


@agent.tool
def lookup_customer(ctx: RunContext[MyDeps], customer_id: str) -> dict | None:
    return ctx.deps.customers.get(customer_id)


@agent.tool
def check_knowledge_base(ctx: RunContext[MyDeps], keyword: str) -> dict | None:
    return ctx.deps.knowledge_base.get(keyword.lower())


@agent.output_validator
async def validate_priority_not_underrated(
    ctx: RunContext[MyDeps], result: TicketClassification
) -> TicketClassification:
    urgent_keywords = [
        "down",
        "outage",
        "broken",
        "crash",
        "data loss",
        "urgent",
        "critical",
    ]
    # If the ticket text has urgent language but the LLM gave it low priority, reject it
    ticket_text = ctx.deps.ticket_text.lower()  # the original user message
    has_urgent_language = any(kw in ticket_text for kw in urgent_keywords)

    if has_urgent_language and result.priority < 3:
        raise ModelRetry(
            "Ticket contains urgent language — priority should be at least 3"
        )

    return result
