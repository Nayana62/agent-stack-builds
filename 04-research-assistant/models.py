from typing import Literal

from pydantic import BaseModel, Field


class Router(BaseModel):
    query_type: Literal["factual", "opinion"]
    reasoning: str = Field(
        description="short reason explaining why is it classified as factual or opinion."
    )


class Research(BaseModel):
    answer: str
    sources: list[str]
    confidence: Literal["high", "medium", "low"]


class Opinion(BaseModel):
    answer: str
    perspective: Literal["balanced", "pro", "con"]
    confidence: Literal["high", "medium", "low"]
