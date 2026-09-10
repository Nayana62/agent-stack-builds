from dataclasses import dataclass

from agent import agent, MyDeps
from mock_data import CUSTOMERS, KNOWLEDGE_BASE, SAMPLE_TICKETS
import time
from pydantic_ai.exceptions import ModelHTTPError

for i, ticket in enumerate(SAMPLE_TICKETS):
    print(f"\n--- Ticket {i + 1} ---")
    print(f"Input: {ticket[:80]}...")
    print("Classifying...")
    try:
        result = agent.run_sync(
            ticket,
            deps=MyDeps(
                customers=CUSTOMERS, knowledge_base=KNOWLEDGE_BASE, ticket_text=ticket
            ),
        )
        print(result.output.model_dump_json(indent=2))
    except ModelHTTPError as e:
        print(f"API error, skipping: {e}")
    time.sleep(5)
