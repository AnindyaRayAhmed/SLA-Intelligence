from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TicketRecord(BaseModel):
    ticket_id: str
    agent_name: str
    created_at: datetime
    first_response_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    status: str
    priority: str
    category: str
    channel: str


class UploadResponse(BaseModel):
    kpis: dict = Field(default_factory=dict)
    charts: dict = Field(default_factory=dict)
    insights: dict = Field(default_factory=dict)
    table_data: list[dict] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
