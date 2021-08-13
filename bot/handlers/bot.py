from pyrogram import filters
from ..config import bot_id
from pyrogram.handlers import MessageHandler

print(bot_id)


def handle_start_reply(client, msg):
    if not msg.reply_to_message:
        return
    userid = int(msg.reply_to_message.text.split(' ')[1])
    msg.forward(userid)


start_reply_handler = MessageHandler(
    handle_start_reply,
    filters.chat(bot_id))
