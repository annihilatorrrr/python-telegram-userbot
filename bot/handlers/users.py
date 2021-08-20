from pyrogram import filters
from pyrogram.handlers import MessageHandler
from ..init import bot
from ..db import User, allowed_users, messages_cache
from ..config import (bot_username, warn_limit,
                      pm_log_group)

from ..utils import (get_users,
                     is_user,
                     get_user)


def send_pm_engine(client, msg):
    res = client.get_inline_bot_results(bot_username,
                                        f'pm_check {msg.from_user.id}')
    return client.send_inline_bot_result(
        msg.chat.id,
        query_id=res.query_id,
        result_id=res.results[0].id,
        hide_via=True
    )


def handle_pm(client, msg):
    from_user = msg.from_user.id
    if from_user in allowed_users:
        return True

    """
        Check if user is in database
        if so increment his warns for recurring PMs.
        If not create an entry for him
    """
    if not is_user(from_user):
        """
            msg_sent is a simple flag to understand that
            this user has already received a forwarded message from
            pmsecurity bot.

            If this flag is true, further messages wont be sent.
        """
        user = User(user_id=from_user, warns=1, allowed=0)
        user.save()
    else:
        user = get_user(from_user)
        user.warns = user.warns + 1
        user.save()

    """
        If PM engine has already been sent, grab its ID and
        delete the message.
    """

    if messages_cache.exists(from_user):
        del_id = messages_cache.get(from_user)
        client.delete_messages(
            chat_id=msg.chat.id,
            message_ids=del_id
        )

    """
        Delete the sender's message.
        Cos otherwise its annoying, no.
    """
    msg.delete()
    """
        Send PM engine and grab the message id
    """
    message = send_pm_engine(client, msg)
    message_id = message.updates[0].id
    """
        Upsert the message id for the user in messages cache
    """
    messages_cache.add(from_user, message_id, replace=True)

    if user.warns >= warn_limit:
        # Block the user as warn limit have increased
        client.send_message(
            from_user,
            text='You have reached all 5 warnings. You will be blocked'
        )
        msg.from_user.block()
        """
            Block notification to PMLog
        """
        client.send_message(
            chat_id=pm_log_group,
            text=(f'{msg.from_user.first_name}({msg.from_user.id})'
                  ' was blocked for reaching maximum warns.')
        )

    # msg.delete()


def handle_approve_user(client, msg):
    """
        Allow a person to PM.
        Can be used inside group or PM.
    """
    if msg.reply_to_message:
        """
            Reply to can work in groups and private. Does not matter unlike the
            next elif block.

            All we need to check is if the user replied to his own message
        """
        user_id = msg.reply_to_message.from_user.id
        """
            Check if the replied to message is from client itself,
            if so stop execution
        """
        # that check goes here lol
    elif not msg.reply_to_message and msg.chat.type == 'private':
        """
            If there is no reply to message and the chat type is private
            just grab the chat id as the user id.

            That 'private' chat check is simply so that sending a .allow
            command in a group without a reply does not make sense

        """
        user_id = msg.chat.id

    if is_user(user_id):
        user = get_user(user_id)
        user.warns = 0
        user.allowed = 1
    else:
        user = User(user_id=user_id,
                    allowed=1,
                    warns=0)

    try:
        user.save()
    except Exception as e:
        print(str(e))
        msg.edit_text('Unexpected error occured. Failed to approve user')

    """
        Lets just call an unblock on the user just to be safe
    """
    try:
        client.unblock_user(user_id)
    except Exception as e:
        """
            User is probably not blocked
        """
        print(str(e))
        pass
    """
        Add approved user to cache
    """
    allowed_users.add(user_id, user, replace=True)
    msg.edit_text('User has been approved')


def handle_block_user(client, msg):
    """
        Block a person from PM-ing.
        Can be used inside group or PM.
    """
    if msg.reply_to_message:
        """
            Reply to can work in groups and private. Does not matter unlike the
            next elif block.

            All we need to check is if the user replied to his own message
        """
        user_id = msg.reply_to_message.from_user.id
        """
            Check if the replied to message is from client itself,
            if so stop execution
        """
        # that check goes here lol
    elif not msg.reply_to_message and msg.chat.type == 'private':
        """
            If there is no reply to message and the chat type is private
            just grab the chat id as the user id.

            That 'private' chat check is simply so that sending a .allow
            command in a group without a reply does not make sense

        """
        user_id = msg.chat.id

    if is_user(user_id):
        user = get_user(user_id)
        user.warns = 5
        user.allowed = 0
    else:
        user = User(user_id=user_id,
                    allowed=0,
                    warns=5)

    try:
        user.save()
    except Exception as e:
        print(str(e))
        msg.edit_text('Unexpected error occured. Failed to approve user')

    """
        Call block on the user
    """
    try:
        client.block_user(user_id)
    except Exception as e:
        """
            User is probably already blocked
        """
        print(str(e))
        pass

    """
        Remove user from allowed_users cache
    """
    allowed_users.remove(user_id)
    msg.edit_text('Person has been blocked')


pm_handler = MessageHandler(
    handle_pm,
    (
        (filters.private & ~filters.me) & ~filters.bot) & ~filters.chat(777000)
    )

approve_user_handler = MessageHandler(
    handle_approve_user,
    filters.command('allow', '.')
)

block_user_handler = MessageHandler(
    handle_block_user,
    filters.command('block', '.')
)
