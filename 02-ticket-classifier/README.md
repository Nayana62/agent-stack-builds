# Ticket Classifier

A PydanticAI agent that reads a free-text customer support ticket, looks up the customer and any relevant help articles, and returns a validated classification — category, priority, summary, and suggested action.

## What does this do?

Support tickets arrive as unstructured text. This agent turns them into structured data an app can actually route on. Given a ticket, it pulls the account ID out of the text and calls `lookup_customer` to find the customer's plan, calls `check_knowledge_base` to find related help articles, then classifies the ticket into a `TicketClassification` model. Because the output type is a Pydantic model, the agent can't return prose — it either returns data in the right shape or retries until it does.

There's also a business rule Pydantic can't express: if the ticket contains urgent language ("down", "outage", "data loss"), a priority below 3 is rejected and the model is asked to try again.

## What I learned building this

- **Structured output with `output_type`** — handing an Agent a Pydantic model makes PydanticAI generate a tool schema from it and validate the model's reply against it. You get typed data back, not a string you have to parse.
- **Dependency injection with `deps_type`** — `MyDeps` carries the customer table, the knowledge base, and the raw ticket text into every tool and validator through `RunContext`. No globals, and tests can pass their own data in.
- **Tools** — `@agent.tool` functions let the model fetch data partway through a run. It decides when to call them from the function signature, so the ticket's account ID drives the lookup.
- **Output validators and `ModelRetry`** — `@agent.output_validator` runs after Pydantic validation, for rules about *meaning* rather than shape. Raising `ModelRetry` sends the model back for another attempt with the complaint attached.
- **Schema constraints beat field validators** — `Field(ge=1, le=5)` becomes part of the JSON Schema the model actually reads, so it gets the range right up front. A `@field_validator` is invisible to the model and only complains afterwards. This one bit me: with a bare `int`, the test model generated `priority=0` and every run burned its retries.
- **Testing an agent without an LLM** — `agent.override(model=TestModel())` swaps in a stub that fabricates output from the schema, and `models.ALLOW_MODEL_REQUESTS = False` makes sure a real API call can never sneak through. `TestModel` is deterministic, so to exercise a specific validator path you pin the output with `custom_output_args` rather than hoping it guesses a useful value.

## How to run

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

The agent runs on Gemini, so add a `.env` with your key:

```
GOOGLE_API_KEY=your-key-here
```

Then classify the sample tickets:

```bash
python main.py
```

It sleeps 5 seconds between tickets to stay under the rate limit, and skips any ticket that returns an API error.

## How to test

```bash
pytest -v
```

The tests use `TestModel` throughout, so they need no API key and make no network calls.

## Project structure

```
├── models.py          # TicketClassification — the structured output model
├── agent.py           # Agent, deps, tools, and the priority output validator
├── main.py            # Runs the agent over the sample tickets
├── mock_data.py       # Fake customers, knowledge base, and sample tickets
├── conftest.py        # Empty — puts the project root on sys.path for tests
├── tests/
│   └── test_agent.py  # Agent tests using TestModel
├── requirements.txt
└── README.md
```
