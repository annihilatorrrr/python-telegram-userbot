from pydantic import BaseModel, Field
from typing import Optional


class FilterSchema(BaseModel):
    message_id: Optional[int]
    filter_text: str
    reply_text: Optional[str]

    def can_copy(self):
        return bool(self.message_id)

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    user_id: int = Field(source='id')
    warns: int = Field(source='warns')
    allowed: int = Field(source='blocked')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class GroupSchema(BaseModel):
    group_id: int
    enabled: bool
    enable_welcome: bool
    enable_leave: bool
    welcome_text: str
    exit_text: str
    remove_service_msg: bool

    class Config:
        orm_mode = True
