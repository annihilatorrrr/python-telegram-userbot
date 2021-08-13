from pyrogram import filters
from pyrogram.handlers import MessageHandler
import urbandict


def prep_message(data):
    data = data[0]
    msg = f'__Word__: **{data["word"]}**\n\n'
    msg = f'{msg}__Definition__:\n```{data["def"]}```'
    return msg


def handle_ud(client, msg):
    if len(msg.command) <= 1:
        return False
    word = ' '.join(msg.command[1:])
    defe = urbandict.define(word)
    msg.edit_text(
        prep_message(defe),
        parse_mode='MARKDOWN'
    )


urbandict_handler = MessageHandler(
    handle_ud,
    filters.command('ud', '.') & filters.me
)
