# LangChain Ticket Classifier

The same support-ticket classifier as [02](../02-ticket-classifier), rebuilt in LangChain instead of PydanticAI — to see what the framework was doing for me.

## What does this do?

Given a free-text support ticket, it pulls the account ID out of the text, calls `lookup_customer` for the customer's plan and history, calls `check_knowledge_base` for related help articles, and returns a validated `TicketClassification` — category, priority 1–5, one-line summary, and suggested action.

The run happens in two phases. First a **gather** phase: the model is bound to the tools and called in a loop — while it asks for tool calls, they're executed, their results appended as `ToolMessage`s, and the model is invoked again on the grown message list. Then a **classify** phase: the same conversation is handed to a second model configured with `with_structured_output(TicketClassification)`, plus a final human turn telling it to classify using what it gathered.

Splitting it in two is the point. A model bound to tools wants to emit tool calls; a model pinned to a structured output wants to emit that one object. Asking for both at once fights itself, so the tools run first and the schema is applied to the finished conversation.

## What I learned building this

- **You own the message list** — in LangChain the conversation *is* the state, and it's yours to maintain. Every model response and every tool result gets appended in order by hand. Forget one and the model silently loses the thread.
- **The tool loop is code you write** — `bind_tools` only tells the model the tools exist. Checking `response.tool_calls`, dispatching each one through a name→tool map, and re-invoking until the model stops asking is a `while` loop you write yourself. PydanticAI ran that loop for me and I never saw it.
- **`tool_call_id` is the wiring** — a `ToolMessage` has to carry the id of the call it answers. That id is how the model matches a result to the request it made, which matters the moment it asks for two tools in one turn.
- **`@tool` reads the signature and docstring** — same idea as PydanticAI's `@agent.tool`: the type hints become the argument schema and the docstring tells the model when to reach for it. Writing "like C-1234" into the docstring is what gets the ID passed in the right format.
- **`with_structured_output` is the whole validation story** — it binds the Pydantic model as the model's response format and gives back typed data. There's no retry-on-invalid-output layer like PydanticAI's `ModelRetry`; if you want the model corrected on a rule Pydantic can't express, that's a loop you build.
- **`ChatPromptTemplate` separates the prompt from the run** — `{ticket}` stays a placeholder until `.invoke()` fills it and `.to_messages()` turns it into the list the model takes.
- **Same task, more surface area** — every piece PydanticAI handled implicitly is now a line I can see and change. That's the trade: more control, more to get wrong.

## How to run

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install langchain-core langchain-google-genai python-dotenv pydantic
```

The model is Gemini, so add a `.env` with your key:

```
GOOGLE_API_KEY=your-key-here
```

Then classify the sample tickets:

```bash
python main.py
```

Each ticket prints its classification as JSON. Any ticket that raises — an API error, a rate limit — is reported and skipped so the rest still run.

## Project structure

```
├── models.py          # TicketClassification — the structured output model
├── tools.py           # lookup_customer and check_knowledge_base, as @tool functions
├── agent.py           # Prompt, bound model, the tool loop, and the structured-output call
├── main.py            # Runs the classifier over the sample tickets
├── mock_data.py       # Fake customers, knowledge base, and sample tickets
├── requirements.txt
└── README.md
```
