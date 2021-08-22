from pyrogram import filters
from pyrogram.handlers import MessageHandler
from ..filters import (allowed_group_filter)
from .. import utils
from ..db import Filter, allowed_groups
from ..config import log_group


def handle_add_filter(client, msg):
    if len(msg.command) <= 1:
        return False
    filter_text = msg.command[1].lower()
    message_id = None
    reply_text = None

    # Check if filter already exists
    q = Filter.select().where(
        (Filter.filter_text == filter_text) & (Filter.group_id == msg.chat.id)
    )

    if q.count():
        msg.edit_text(f'Filter already exists for {filter_text}')
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
               message_id=message_id,
               group_id=msg.chat.id)
    f.save()
    group = utils.get_group(msg.chat.id)
    allowed_groups.add(msg.chat.id, group, replace=True)
    msg.edit_text(f'Filter saved for {filter_text}')


def handle_remove_filter(client, msg):
    if len(msg.command) <= 1:
        return False
    filter_text = msg.command[1]

    q = Filter.select().where(
        (Filter.filter_text == filter_text) & (Filter.group_id == msg.chat.id)
    )

    if not q.count():
        msg.edit_text(f'Filter does not exist for {filter_text}')
        return False

    q = q[0].delete_instance()
    group = utils.get_group(msg.chat.id)
    allowed_groups.add(msg.chat.id, group, replace=True)
    msg.edit_text(f'Filter removed for {filter_text}')


def process_filter(client, msg):
    group_id = msg.chat.id

    msg_text = msg.text or msg.caption
    if msg_text:
        msg_tokens = set(msg_text.lower().split(' '))
        group = allowed_groups.get(group_id)
        filter_tokens = set([f.filter_text for f in group.filters])
        token_matches = filter_tokens.intersection(msg_tokens)
        if not len(token_matches):
            return False
        # get the first match
        token_matches = list(token_matches)
        token_match = token_matches[0]
        matched_filters = [
            f for f in group.filters if f.filter_text == token_match
        ]
        if not len(matched_filters):
            return False
        matched_filter = matched_filters[0]

        if matched_filter.can_copy():
            """
                Its a copy-able message so just copy it into the current chat
            """
            client.copy_message(
                from_chat_id=log_group,
                chat_id=msg.chat.id,
                message_id=matched_filter.message_id,
                reply_to_message_id=msg.message_id
            )
        else:
            """
                Its a text reply based filter.
                Simply reply with the text
            """
            msg.reply_text(matched_filter.reply_text)


add_filter_handler = MessageHandler(
    handle_add_filter,
    (filters.command('filter', '.') & filters.me)
    & allowed_group_filter
)

rm_filter_handler = MessageHandler(
    handle_remove_filter,
    (filters.command('rmfilter', '.') & filters.me)
    & allowed_group_filter
)

process_filter_handler = MessageHandler(
    process_filter,
    (
        (filters.media | filters.text) & (~filters.me & ~filters.private)
        & allowed_group_filter
    )
)
