from pyrogram import filters
from pyrogram.handlers import MessageHandler
from ..filters import allowed_group_filter
from ..db import Filter, message_filters
from ..config import log_group


def handle_add_filter(client, msg):
    if len(msg.command) <= 1:
        return False
    filter_text = msg.command[1].lower()
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
    message_filters.add(filter_text, f, replace=True)
    msg.edit_text(f'Filter saved for {filter_text}')


def handle_remove_filter(client, msg):
    if len(msg.command) <= 1:
        return False
    filter_text = msg.command[1]

    q = Filter.select().where(Filter.filter_text == filter_text)
    if not q.count():
        msg.edit_text(f'Filter does not exist for {filter_text}')
        return False

    q = q[0].delete_instance()
    message_filters.remove(filter_text)
    msg.edit_text(f'Filter removed for {filter_text}')


def process_filter(client, msg):
    msg_text = msg.text or msg.caption
    # msg_text = msg_text.lower()
    if msg_text:
        msg_text = msg_text.lower()
        """
            Cast all of this to set to check intersection
            to see if the message contains any words that
            trigger a defined filter
        """
        filter_keys = [key.lower() for key in message_filters.allkeys()]
        filter_keys = set(filter_keys)
        text_words = set(msg_text.split(' '))
        """
            Get all matched filters
        """
        intersection = filter_keys.intersection(text_words)
        print(intersection)
        if not len(intersection):
            return False
        matches = list(intersection)
        """
            Get the first matched filter
        """
        filter_text = matches[0]
        try:
            filterr = message_filters.get(filter_text)
        except Exception:
            return False

        if filterr.can_copy():
            """
                Copy the message if its a presaved message for the filter
            """
            # copy message
            client.copy_message(
                from_chat_id=log_group,
                chat_id=msg.chat.id,
                message_id=filterr.message_id,
                reply_to_message_id=msg.message_id
            )
        else:
            """
                If not just send the defined reply_text for the filter
            """
            msg.reply_text(filterr.reply_text)
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
    (
        (filters.media | filters.text) & (~filters.me & ~filters.private)
        & allowed_group_filter
    )
)
