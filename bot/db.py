from .schema import UserSchema, FilterSchema, GroupSchema
from .cache import Cache
from peewee import (
    Model,
    BigIntegerField,
    TextField,
    BooleanField,
    ForeignKeyField,
    SqliteDatabase
)

allowed_users = Cache(UserSchema)
message_filters = Cache(FilterSchema)
allowed_groups = Cache(GroupSchema)
messages_cache = Cache()
processed_cache = []


def clear_processed_cache():
    processed_cache.clear()


db = SqliteDatabase('data.db')


class Group(Model):
    """
        Below exit message refers to a goodbye message that the
        userbot will send when a user leaves a group chat.
    """
    group_id = BigIntegerField(unique=True)
    enabled = BooleanField()
    enable_welcome = BooleanField()  # Are welcome messages enabled ?
    enable_leave = BooleanField()  # Are exit messages enabled
    remove_service_msg = BooleanField()
    welcome_text = TextField(default='Welcome to the group {user}')
    exit_text = TextField(default='Goodbye, {user}')

    class Meta:
        database = db


class Filter(Model):
    message_id = BigIntegerField(null=True, default=None)
    filter_text = TextField(null=True)
    reply_text = TextField(null=True, default=None)
    group_id = ForeignKeyField(model=Group,
                               field='group_id',
                               backref='filters',
                               lazy_load=False)

    class Meta:
        database = db


class User(Model):
    user_id = BigIntegerField(unique=True)
    warns = BigIntegerField()
    allowed = BooleanField()

    class Meta:
        database = db


db.create_tables([Filter, User, Group])
