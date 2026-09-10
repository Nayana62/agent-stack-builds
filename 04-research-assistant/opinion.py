from dotenv import load_dotenv
from pydantic_ai import Agent
from models import Opinion

load_dotenv()

agent = Agent(
    "google:gemini-3.6-flash",
    instructions="""You are a thoughtful analyst. When given a question that requires judgment or opinion:

1. Consider multiple angles before answering
2. Give a clear, balanced analysis
3. Set perspective to "balanced" if you present multiple sides, "pro" if you argue in favor, "con" if you argue against
4. Set confidence to "high" if this is a well-understood topic, "medium" if reasonable people disagree, "low" if it's highly subjective
""",
    output_type=Opinion,
)
