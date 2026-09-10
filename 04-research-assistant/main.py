from pydantic_ai import ModelHTTPError
from router import agent as router_agent
from researcher import agent as researcher_agent, ResearchDeps
from opinion import agent as opinion_agent
from mock_data import SEARCH_RESULTS

SAMPLE_QUESTIONS = [
    "What is the capital of France?",
    "Should I learn Rust or Go for backend development?",
    "When was Python created?",
    "Is remote work better than working from an office?",
]

for question in SAMPLE_QUESTIONS:
    print(f"\nQuestion: {question}")

    try:
        router_result = router_agent.run_sync(question)
        print(router_result.output.model_dump_json(indent=2))

        if router_result.output.query_type == "factual":
            result = researcher_agent.run_sync(
                question, deps=ResearchDeps(search_data=SEARCH_RESULTS)
            )
            print(result.output.model_dump_json(indent=2))
        else:
            result = opinion_agent.run_sync(question)
            print(result.output.model_dump_json(indent=2))

    except ModelHTTPError as e:
        print(f"API error, skipping: {e}")
