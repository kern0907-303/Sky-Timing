# schemas.py
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

class DailyStateResponse(BaseModel):
    date: str
    timezone: str
    city: str
    raw_timing_data: Dict[str, Any]
    semantic_vectors: Dict[str, float]
    primary_force: str
    secondary_force: str
    constraint_force: str
    daily_rhythm: str
    daily_summary: str
    reflection_question: str
    created_at: str

class GenerateRequest(BaseModel):
    date: str = Field(description="ISO Date YYYY-MM-DD")
    timezone: str = "Asia/Taipei"
    city: str = "Taipei"

class AskRequest(BaseModel):
    question: str = Field(description="我正在考慮什麼")
    event_type: str = Field(description="事件類型")
    constraint: str = Field(description="目前最大限制")
    date: str = Field(description="查詢日期 YYYY-MM-DD")

class FeedbackRequest(BaseModel):
    date: str = Field(description="反饋日期 YYYY-MM-DD")
    reaction: str = Field(description="反饋反應: resonant, partial, not_resonant")
    observation: Optional[str] = Field(default=None, max_length=200, description="觀察內容，最多200字")
    anonymous_session_id: str = Field(description="匿名會話ID")
