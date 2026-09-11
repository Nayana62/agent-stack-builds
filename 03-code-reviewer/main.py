import time

from pydantic_ai import ModelHTTPError
from agent import agent, number_lines
from mock_data import SAMPLE_FUNCTIONS

for label, code in SAMPLE_FUNCTIONS.items():
    print(f"\n--- Sample: {label} ---")
    print(code)
    print("Reviewing...")
    try:
        result = agent.run_sync(number_lines(code))
        print(result.output.model_dump_json(indent=2))
    except ModelHTTPError as e:
        print(f"API error, skipping: {e}")
    time.sleep(5)
