from pydantic import BaseModel
from typing import List, Optional


class ActionItem(BaseModel):
    owner: str
    task: str
    due_date: Optional[str]
    flag: Optional[str]


class MeetingMinutes(BaseModel):
    summary: List[str]
    decisions: List[str]
    action_items: List[ActionItem]
    pending_questions: List[str]
    unclear_commitments: List[str]