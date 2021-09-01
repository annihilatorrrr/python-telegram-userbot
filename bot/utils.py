from pyrogram.types import (
    InlineKeyboardMarkup as Kb,
    InlineKeyboardButton as Button
)
from .db import (Filter,
                 User,
                 Group,
                 allowed_users,
                 message_filters,
                 allowed_groups)
import hashlib


def get_message_filters():
    data = {}
    for x in Filter.select():
        cfg = {}
        if x.message_id:
            cfg['message_id'] = x.message_id
        else:
            cfg['reply_text'] = x.reply_text
        data[x.filter_text] = cfg
    return data


def hashed_msg_id(chat_id, message_id):
    """
        Returns a sha1 hash of group_id+msg_id

        This hash is used to identify a message that has been processed by
        the handler that deals with processing filters. There is an issue where
        the message is handled twice in super groups.
        (Try webhooks, looser.)
    """
    hash_ = (str(chat_id) + str(message_id)).encode()
    return hashlib.sha1(hash_).hexdigest()


def unblock_keyboard(user_id):
    return Kb(
        [
            [
                Button('Unblock', callback_data=f'unblock_user {user_id}')
            ]
        ]
    )


def process_group_info(group):
    """
        You might be thinking what kind of idiot concats strings like this
        when there's clearly f-strings.
        I think f-strings look ugly in some cases. This is one of them.
    """
    NEWLINE = '\n'
    bool_dict = {
        True: 'Enabled',
        False: 'Disabled'
    }
    retrieve = bool_dict.get
    output = (
        '<b>Welcome greeting</b>: <i>{welcome_greeting}</i>' + NEWLINE +
        '<b>Leave greeting</b>: <i>{leave_greeting}</i>' + NEWLINE +
        '<b>Welcome text</b>: <i>{welcome_text}</i>' + NEWLINE +
        '<b>Leave text</b>: <i>{leave_text}</i>' + NEWLINE +
        '<b>Remove service messages</b>: <i>{rm_enabled}</i>' + NEWLINE
    )
    return output.format(
        welcome_greeting=retrieve(group.enable_welcome),
        leave_greeting=retrieve(group.enable_leave),
        welcome_text=group.welcome_text,
        leave_text=group.exit_text,
        rm_enabled=retrieve(group.remove_service_msg)
    )


def load_allowed_groups():
    """
        Load all allowed groups into cache on startup
    """
    for group in Group.select():
        allowed_groups.add(group.group_id, group)


def load_message_filters():
    """
        Load all configured message filters into cache on startup
    """
    for filt in Filter.select():
        message_filters.add(
            filt.filter_text,
            filt,
            replace=True
        )


def load_allowed_users():
    """
        Loads all allowed users into cache on startup
    """
    for user in User.select().where(
        User.allowed == 1
    ):
        allowed_users.add(user.user_id, user)


def get_group(group_id):
    q = Group.select().where(Group.group_id == group_id)
    if not q.count():
        return False
    return q.get()


def get_users(allowed: bool):
    data = []
    for x in User.select(User.user_id).where(
        User.allowed == allowed
    ):
        data.append(x.user_id)
    return data


def is_user(user_id: int):
    """
        Check if the user exists in the database
    """
    return User.select().where(User.user_id == user_id).count()


def get_user(user_id: int):
    """
        Return User's peewee model instance
    """
    return User.select().where(User.user_id == user_id).get()


def allow_user(user_id: int):
    user = User.select().where(
        User.user_id == user_id
    )

    """
        If user does not exist
        create a new one record
    """
    if not user.count():
        user = User(user_id=user_id,
                    allowed=1,
                    warns=0
                    )
        try:
            user.save()
        except Exception:
            raise
    else:
        user = get_user(user_id)
        user.warns = 0
        user.allowed = 1
        try:
            user.save()
        except Exception:
            raise
    return user


def block_user(user_id: int):
    if not is_user(user_id):
        user = User(
            user_id=user_id,
            allowed=0,
            warns=5
        )
        try:
            user.save()
        except Exception:
            raise
    else:
        user = get_user(user_id)
        user.warns = 5
        user.allowed = 0
        try:
            user.save()
        except Exception:
            raise

    return user


def get_user_warns(user_id: int):
    """
        Get the warns of a user
    """
    return (
        User.select().where(User.user_id == user_id)
        .get()
        .warns)
