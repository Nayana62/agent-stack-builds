from agent import classify_ticket
from mock_data import SAMPLE_TICKETS

for i, ticket in enumerate(SAMPLE_TICKETS):
    print(f"\n--- Ticket {i + 1} ---")
    print(f"Input: {ticket[:80]}...")
    print("Classifying...")
    try:
        result = classify_ticket(ticket=ticket)
        print(result.model_dump_json())
    except Exception as e:
        print(f"API error, skipping: {e}")
