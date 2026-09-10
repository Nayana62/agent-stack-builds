from dotenv import load_dotenv
from pydantic_ai import Agent
from models import Router

load_dotenv()

agent = Agent(
    "google:gemini-3.6-flash",
    instructions="""You are a query classifier. Decide whether a user's question is factual or opinion-based.

Factual: the question has a concrete, verifiable answer that could be looked up (dates, definitions, statistics, how something works).

Opinion: the question requires analysis, comparison, personal judgment, or a recommendation. There's no single "right" answer.

Use the reasoning field to explain your classification in one sentence.
""",
    output_type=Router,
)
