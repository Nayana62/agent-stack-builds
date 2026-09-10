from dataclasses import dataclass, field
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from models import Research
from mock_data import SEARCH_RESULTS

load_dotenv()


@dataclass
class ResearchDeps:
    search_data: dict = field(default_factory=lambda: SEARCH_RESULTS)


agent = Agent(
    "google:gemini-3.6-flash",
    instructions="""You are a research assistant. When given a factual question:

1. Use the web_search tool with relevant keywords from the question
2. Read the search results carefully
3. Synthesize a clear, concise answer based on what you found
4. Include the URLs from the results you used as sources
5. Set confidence to "high" if multiple sources agree, "medium" if only one source, "low" if results are vague or conflicting
""",
    output_type=Research,
    deps_type=ResearchDeps,
)


@agent.tool
def web_search(ctx: RunContext[ResearchDeps], query: str) -> list[dict]:
    """Search the web for information about the query."""
    results = []
    for keyword, entries in ctx.deps.search_data.items():
        if keyword in query.lower():
            results.extend(entries)
    if not results:
        results = ctx.deps.search_data.get("default", [])
    return results
