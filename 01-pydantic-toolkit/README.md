# Pydantic Toolkit

A Pydantic-based toolkit for defining, validating, and managing AI agent tool definitions, including a registry with JSON persistence and JSON schema generation.

## What this demonstrates

- Pydantic models (`Tool`, `ToolParameter`) with field constraints and custom `field_validator`s (snake_case name enforcement, non-empty parameter lists)
- Type coercion and validation errors surfaced through `pydantic.ValidationError`
- A `ToolRegistry` for adding, removing, looking up, and searching tool definitions
- Generating JSON Schema from a model with `model_json_schema()`
- Persisting a registry to disk and reloading it with `model_dump()` / JSON round-tripping

## How to run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python registry.py
```

## How to test

```bash
pytest
```
