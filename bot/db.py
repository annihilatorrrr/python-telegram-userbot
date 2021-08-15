from .schema import UserSchema, FilterSchema
from .cache import Cache
from peewee import (
    Model,
    BigIntegerField,
    TextField,
    BooleanField,
    SqliteDatabase
)

allowed_users = Cache(UserSchema)
message_filters = Cache(FilterSchema)

db = SqliteDatabase('data.db')


class Filter(Model):
    message_id = BigIntegerField(null=True, default=None)
    filter_text = TextField(null=True)
    reply_text = TextField(null=True, default=None)

    class Meta:
        database = db


class User(Model):
    user_id = BigIntegerField(unique=True)
    warns = BigIntegerField()
    # banned or not
    allowed = BooleanField()

    class Meta:
        database = db


db.create_tables([Filter, User])
