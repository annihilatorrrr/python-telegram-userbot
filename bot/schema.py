from pydantic import BaseModel, Field
from typing import Optional, List


class FilterSchema(BaseModel):
    message_id: Optional[int]
    filter_text: str
    reply_text: Optional[str]


class UserSchema(BaseModel):
    user_id: int = Field(source='id')
    warns: int = Field(source='warns')
    allowed: int = Field(source='blocked')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
