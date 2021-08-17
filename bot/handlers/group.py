from pyrogram import filters
from pyrogram.handlers import MessageHandler
from ..db import allowed_groups, Group
from ..filters import allowed_group_filter
from logzero import logger


def handle_join(client, msg):
    mentions = []
    for user in msg.new_chat_members:
        mentions.append(user.mention)
    mentions = ','.join(mentions)
    text = f'Hello and welcome {mentions}'
    try:
        client.send_message(msg.chat.id, text, parse_mode="HTML")
    except Exception as e:
        logger.error(str(e))

    msg.delete()


def handle_chat_id(client, msg):
    msg.edit_text(msg.chat.id)


def handle_leave(client, msg):
    msg.delete()


def handle_allow_group(client, msg):
    q = Group.select().where(
        Group.group_id == msg.chat.id
    )

    if q.count():
        msg.delete()
        return

    g = Group(group_id=msg.chat.id)
    g.save()
    allowed_groups.add(msg.chat.id, msg.chat.id, replace=True)
    msg.delete()


def handle_disallow_group(client, msg):
    q = Group.select().where(
        Group.group_id == msg.chat.id
    )

    if not q.count():
        msg.delete()
        return

    try:
        Group.delete().where(Group.group_id == msg.chat.id).execute()
        allowed_groups.remove(msg.chat.id)
    except Exception as e:
        print(str(e))

    msg.delete()


def handle_random(client, msg):
    print('i got random')


new_member_handler = MessageHandler(
    handle_join,
    ((filters.new_chat_members & ~filters.me) & allowed_group_filter)
)

new_member_handler = MessageHandler(
    handle_leave,
    ((filters.left_chat_member & ~filters.me) & allowed_group_filter)
)

get_chatid_handler = MessageHandler(
    handle_chat_id,
    filters.command('chat_id', '.') & filters.me
)

allow_group_handler = MessageHandler(
    handle_allow_group,
    (filters.command('allow_group', '.') & filters.me) & ~filters.private
)

disallow_group_handler = MessageHandler(
    handle_disallow_group,
    (filters.command('block_group', '.') & filters.me) & ~filters.private
)

random_handler = MessageHandler(
    handle_random,
    ((filters.command('random', '.') & filters.me) & allowed_group_filter)
)
