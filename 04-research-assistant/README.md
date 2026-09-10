# Research Assistant

Three PydanticAI agents behind a router: a classifier decides whether a question is factual or opinion-based, then hands it to a researcher that searches for sources or to an analyst that reasons it out.

## What does this do?

One agent with one giant prompt has to be good at everything. This project splits the work instead. A small `Router` agent reads the question and returns a `query_type` of `"factual"` or `"opinion"` plus a one-line reason. `main.py` branches on that:

- **Factual** → the researcher agent, which calls a `web_search` tool over mocked search results, synthesises an answer, and returns it with the source URLs and a confidence level.
- **Opinion** → the analyst agent, which has no tools and returns an answer, the perspective it took (`balanced` / `pro` / `con`), and a confidence level.

Each branch has its own output model, so the shape of the result tells you which path ran — `Research` carries `sources`, `Opinion` carries `perspective`. The orchestration is plain Python control flow, not a framework graph.

## What I learned building this

- **Routing beats one big prompt** — a cheap classification step lets each downstream agent have short, focused instructions. The researcher never has to be told what to do with an opinion question, because it never sees one.
- **`Literal` is a real constraint, not a hint** — `Literal["factual", "opinion"]` becomes an enum in the JSON Schema the model reads, so it can only answer with one of those two strings. That's what makes `if router_result.output.query_type == "factual"` safe to branch on without any string cleanup.
- **`Field(description=...)` is prompt text** — the description on `Router.reasoning` travels into the schema, so it's another place to tell the model what you want. Instructions aren't only in `instructions`.
- **Asking for reasoning alongside the label** — the `reasoning` field costs one extra sentence and makes a wrong classification obvious immediately, instead of leaving you guessing why the wrong agent ran.
- **Deps go only where they're needed** — the researcher takes `ResearchDeps` because its tool needs a search index it can be handed; the router and analyst take no deps at all. Uniformity for its own sake would just be noise.
- **Give a tool a fallback** — `web_search` matches keywords against the mock data and drops to the `"default"` entry when nothing hits, so the agent always gets a list back. A tool that returns nothing leaves the model to invent something.
- **One agent module, one concern** — `router.py`, `researcher.py`, and `opinion.py` each own an agent and its instructions; `main.py` only wires them together. Swapping a model or rewriting a prompt touches one file.
- **Failures shouldn't be fatal** — catching `ModelHTTPError` per question means a rate limit on question two doesn't cost you questions three and four.

## How to run

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install pydantic-ai python-dotenv
```

All three agents run on Gemini, so add a `.env` with your key:

```
GOOGLE_API_KEY=your-key-here
```

Then run the sample questions through the router:

```bash
python main.py
```

It prints the router's classification and then the output of whichever agent handled the question, both as JSON.

## Project structure

```
├── models.py          # Router, Research, Opinion — one output model per agent
├── router.py          # Classifier agent — factual or opinion
├── researcher.py      # Research agent, its deps, and the web_search tool
├── opinion.py         # Analyst agent — no tools, judgement only
├── main.py            # Routes each sample question to the right agent
├── mock_data.py       # Fake search results keyed by topic
└── README.md
```
