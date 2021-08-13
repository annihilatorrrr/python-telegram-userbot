from pydantic import BaseModel
from typing import Optional, List


class FilterSchema(BaseModel):
    message_id: Optional[int]
    filter_text: str
    reply_text: Optional[str]
