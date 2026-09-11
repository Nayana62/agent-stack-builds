# Code Reviewer

A PydanticAI agent that reads the source of a Python function and returns a structured review — a list of issues with severities and line numbers, an overall quality rating, concrete suggestions, and a short summary.

## What does this do?

You hand the agent a Python function as a string. It checks for bugs, style problems, missing type hints, weak error handling, and readability issues, and calls a `check_naming_convention` tool to verify the function name is snake_case. The result is a `CodeReview` model, not prose:

- `issues` — each one an `Issue` with a `description`, a `severity` (`critical` / `warning` / `suggestion`), and an optional `line_reference`
- `overall_quality` — `good`, `needs_improvement`, or `poor`
- `suggestions` — actionable one-line improvements
- `summary` — one or two sentences

Before the code goes to the model, `number_lines` prefixes every line with its number, so the model can cite `"line 4"` instead of counting lines itself.

## What I learned building this

- **Nested output models** — `CodeReview.issues` is a `list[Issue]`, and PydanticAI validates the whole tree. A single bad severity deep inside the list fails validation and triggers a retry, same as a bad top-level field.
- **`StrEnum` vs `Literal`** — both become an `enum` in the JSON Schema the model reads. `StrEnum` also gives the values a name in code (`Severity.CRITICAL`), which is handy for filtering issues or asserting in tests.
- **`tool_plain` for tools that don't need context** — `check_naming_convention` is a pure function of its input, so it takes no `RunContext` and the agent takes no deps. Because the decorator returns the original function, it can be unit tested directly.
- **Give the model data, don't make it count** — LLMs are bad at counting lines. Numbering them in the prompt makes `line_reference` reliable for free.
- **`defer_model_check=True`** — without it, creating the agent builds a Gemini client right away and fails when no API key is set, which breaks tests before `TestModel` can be swapped in. Deferring that check makes the tests truly key-free.
- **Tell the model it's allowed to find nothing** — without "don't invent problems" in the instructions, a reviewer will pad a clean function with nitpicks.

## How to run

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

The agent runs on Gemini, so add a `.env` with your key (`GEMINI_API_KEY` also works):

```
GOOGLE_API_KEY=your-key-here
```

Then review the three sample functions — one clean, one with bugs, one messy:

```bash
python main.py
```

It sleeps 5 seconds between samples to stay under the rate limit, and skips any sample that returns an API error.

## How to test

```bash
pytest -v
```

The tests use `TestModel` throughout, so they need no API key and make no network calls.

## Project structure

```
├── models.py          # CodeReview, Issue, Severity, Quality — the structured output
├── agent.py           # Agent, the check_naming_convention tool, and number_lines
├── main.py            # Runs the agent over the sample functions
├── mock_data.py       # Three sample functions: clean, has issues, messy
├── conftest.py        # Empty — puts the project root on sys.path for tests
├── tests/
│   └── test_agent.py  # Agent and tool tests using TestModel
├── requirements.txt
└── README.md
```
