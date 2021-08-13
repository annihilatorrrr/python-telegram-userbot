from .db import Filter, User


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


def get_users(allowed: bool):
    data = []
    for x in User.select(User.user_id).where(
        User.allowed == allowed
    ):
        data.append(x.user_id)
    return data
