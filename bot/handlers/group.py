from pyrogram import filters
from pyrogram.handlers import MessageHandler
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


new_member_handler = MessageHandler(
    handle_join,
    filters.new_chat_members & ~filters.me
)

new_member_handler = MessageHandler(
    handle_leave,
    filters.left_chat_member & ~filters.me
)

get_chatid_handler = MessageHandler(
    handle_chat_id,
    filters.command('chat_id', '.') & filters.me
)
