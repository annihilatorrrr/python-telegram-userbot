from pyrogram import filters
from pyrogram.handlers import MessageHandler
from ..db import User
from ..config import bot_username, warn_limit
from ..utils import (get_users,
                     is_user,
                     get_user)

allowed_users = get_users(allowed=True)


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
        msg_sent = False
        user = User(user_id=from_user, warns=1, allowed=0)
        user.save()
    else:
        msg_sent = True
        user = get_user(from_user)
        user.warns = user.warns + 1
        user.save()

    if not msg_sent:
        res = client.get_inline_bot_results(bot_username,
                                            f'pm_check {from_user}')
        client.send_inline_bot_result(
            msg.chat.id,
            query_id=res.query_id,
            result_id=res.results[0].id,
            hide_via=True
        )

    if user.warns >= warn_limit:
        # Block the user as warn limit have increased
        client.send_message(
            from_user,
            text='You have reached all 5 warnings. You will be blocked'
        )
        msg.from_user.block()


pm_handler = MessageHandler(
    handle_pm,
    (filters.private & ~filters.me) & ~filters.bot)
