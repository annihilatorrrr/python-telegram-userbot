import peewee
from pydantic import BaseModel, Field
from typing import Optional, List, Any
from pydantic.utils import GetterDict


class PeeweeGetterDict(GetterDict):
    """
        For more information about this class
        see https://fastapi.tiangolo.com/advanced/sql-databases-peewee/
    """
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class FilterSchema(BaseModel):
    message_id: Optional[int]
    filter_text: str
    reply_text: Optional[str]
    group_id: int

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
    filters: List[FilterSchema] = Field(default=[])

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
