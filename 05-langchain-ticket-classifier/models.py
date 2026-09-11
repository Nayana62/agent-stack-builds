from typing import Literal

from pydantic import BaseModel, Field, field_validator


class TicketClassification(BaseModel):
    category: Literal["account", "billing", "technical", "general"]
    priority: int = Field(ge=1, le=5)
    summary: str = Field(
        max_length=100, description="A brief one-line summary of the ticket"
    )
    suggested_action: str
