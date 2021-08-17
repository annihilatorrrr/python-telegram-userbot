from .db import (Filter,
                 User,
                 allowed_users,
                 message_filters,
                 allowed_groups)


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


def load_allowed_groups():
    """
        Load all allowed groups into cache on startup
    """
    for group in Filter.select():
        allowed_groups.add(group.id, group.id)


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
