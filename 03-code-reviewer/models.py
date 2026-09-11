from enum import StrEnum

from pydantic import BaseModel, Field


class Severity(StrEnum):
    CRITICAL = "critical"
    WARNING = "warning"
    SUGGESTION = "suggestion"


class Quality(StrEnum):
    GOOD = "good"
    NEEDS_IMPROVEMENT = "needs_improvement"
    POOR = "poor"


class Issue(BaseModel):
    description: str
    severity: Severity
    line_reference: str | None = Field(
        default=None, description="The line the issue is on, e.g. 'line 3'"
    )


class CodeReview(BaseModel):
    issues: list[Issue]
    overall_quality: Quality
    suggestions: list[str]
    summary: str = Field(description="One or two sentences summarising the review")
