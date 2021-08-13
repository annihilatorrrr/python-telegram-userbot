from pyrogram import filters
from pyrogram.handlers import MessageHandler
from .. import utils
from ..db import Filter
from ..config import log_group
from logzero import logger

message_filters = utils.get_message_filters()


def handle_add_filter(client, msg):
    global message_filters
    if len(msg.command) <= 1:
        return False
    filter_text = msg.command[1]
    message_id = None
    reply_text = None

    # Check if filter already exists
    q = Filter.select().where(Filter.filter_text == filter_text)

    if q.count():
        msg.edit_text(f'Fitler already exists for {filter_text}')
        return False

    if msg.reply_to_message:
        c_msg = msg.reply_to_message.copy(log_group)
        message_id = c_msg.message_id
    else:
        if len(msg.command) <= 2:
            return False
        reply_text = ' '.join(msg.command[2:])

    f = Filter(filter_text=filter_text,
               reply_text=reply_text,
               message_id=message_id)
    f.save()
    msg.edit_text(f'Filter saved for {filter_text}')
    message_filters = utils.get_message_filters()


def handle_remove_filter(client, msg):
    global message_filters
    if len(msg.command) <= 1:
        return False
    filter_text = msg.command[1]

    q = Filter.select().where(Filter.filter_text == filter_text)
    if not q.count():
        msg.edit_text(f'Filter does not exist for {filter_text}')
        return False

    q = q[0].delete_instance()
    msg.edit_text(f'Filter removed for {filter_text}')
    message_filters = utils.get_message_filters()


def process_filter(client, msg):
    msg_text = msg.text or msg.caption
    if msg_text:
        try:
            filter_ = message_filters[msg_text]
            if 'message_id' in filter_:
                client.copy_message(
                    from_chat_id=log_group,
                    chat_id=msg.chat.id,
                    message_id=filter_['message_id'],
                    reply_to_message_id=msg.message_id
                )
            elif 'reply_text' in filter_:
                try:
                    msg.reply_text(filter_['reply_text'])
                except Exception as e:
                    logger.error(str(e))
        except KeyError:
            pass
    msg.continue_propagation()


add_filter_handler = MessageHandler(
    handle_add_filter,
    filters.command('filter', '.') & filters.me
)

rm_filter_handler = MessageHandler(
    handle_remove_filter,
    filters.command('rmfilter', '.') & filters.me
)

process_filter_handler = MessageHandler(
    process_filter,
    (filters.media | filters.text) & ~filters.me
)
