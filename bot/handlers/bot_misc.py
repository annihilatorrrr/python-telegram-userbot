from ..config import (owner_id,
                      warn_limit,
                      pm_log_group,
                      about_me)
from ..db import allowed_users, User
from ..utils import (allow_user,
                     block_user,
                     is_user,
                     get_user_warns)
from ..init import userbot
from pyrogram import filters
from pyrogram.types import (InlineKeyboardButton,
                            InlineKeyboardMarkup,
                            InlineQueryResultArticle,
                            InputTextMessageContent)
from pyrogram.handlers import (
        InlineQueryHandler,
        CallbackQueryHandler
)


def deny_access(msg):
    msg.answer(
        results=[],
        switch_pm_text='You are not authorized to use this bot.',
        switch_pm_parameter='createown',
        cache_time=0,
        is_personal=1,
    )
    return True


def send_pm_engine(msg):
    user_id = int(msg.query.split(' ')[1])
    user = User.select().where(User.user_id == user_id)
    if not user.count():
        warns = 1
    else:
        user = user.get()
        warns = user.warns
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text='Warns', callback_data='warns_me'),
                InlineKeyboardButton(text=f'{warns}/5',
                                     callback_data='warns_me'),
            ],
            [
                InlineKeyboardButton(text='Contact me',
                                     callback_data='contact_me'),

                InlineKeyboardButton(text='About',
                                     callback_data='about_me'),
            ]
        ]
    )
    answer = InlineQueryResultArticle(
        title='PM Security',
        input_message_content=InputTextMessageContent(
            'Hold it right there. I don\'t know you.\nWhat is your purpose?'
        ),
        reply_markup=keyboard
    )
    msg.answer([answer], cache_time=0, is_personal=0)


def handle_pm_check(client, msg):
    userid = msg.from_user.id
    if userid != owner_id:
        print('owner mismatch')
        return deny_access(msg)

    send_pm_engine(msg)


def handle_warns_check(client, msg):
    userid = msg.from_user.id
    if not is_user(userid):
        return False
    warns = get_user_warns(userid)
    msg.answer(
        text=f'You have {warns}/{warn_limit} warnings.'
    )


def handle_contact_me(client, msg):
    user_id = msg.from_user.id

    mention = msg.from_user.mention
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text='Approve',
                                     callback_data=f'approve_user {user_id}'),
                InlineKeyboardButton(text='Deny',
                                     callback_data=f'deny_user {user_id}'),
            ]
        ]
    )
    client.send_message(
        pm_log_group,
        text=f'{mention} would like to contact you',
        reply_markup=keyboard,
        parse_mode='HTML'
    )
    msg.answer(
        'Owner has been notified.'
    )


def handle_about_me(client, msg):
    msg.answer(about_me)


def handle_deny_user(client, msg):
    try:
        user = int(msg.data.split(' ')[1])
    except (IndexError, ValueError):
        return
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text='Unblock',
                                     callback_data=f'unblock_user {user}')
            ]
        ]
    )
    """
        Update the entires in db
    """
    user_m = block_user(user)
    """
        Block the user in telegram
    """
    userbot.block_user(user)
    """
        Remove from allowed users cache if exists
    """
    allowed_users.remove(user)
    msg.edit_message_text(
        text='This user has been blocked',
        reply_markup=keyboard
    )


def handle_approve_user(client, msg):
    try:
        user = int(msg.data.split(' ')[1])
    except (IndexError, ValueError):
        return

    try:
        user_m = allow_user(user)
    except Exception as e:
        msg.answer('Unexpected error occured')
        print(str(e))
        return

    msg.edit_message_text(
        text='This user has been approved.'
    )
    """
        Call unblock on this user just to be safe
    """
    try:
        userbot.unblock_user(user)
    except Exception as e:
        print(str(e))
        pass

    """
        Add user into allowed users cache
    """
    allowed_users.add(user, user_m, replace=True)
    userbot.send_message(
        chat_id=user,
        text='You have been approved.'
    )


def handle_unblock_user(client, msg):
    try:
        user = int(msg.data.split(' ')[1])
    except (IndexError, ValueError):
        return

    try:
        user_m = allow_user(user)
    except Exception as e:
        msg.answer('Unexpected error occured')
        print(str(e))
        return

    userbot.unblock_user(user)
    msg.edit_message_text(
        text='This user has been unblocked',
    )
    """
        Add user into allowed users cache
    """
    allowed_users.add(user, user_m, replace=True)
    userbot.send_message(
        chat_id=user,
        text='You have been approved.'
    )


pm_check_handler = InlineQueryHandler(
    handle_pm_check,
    filters.regex('pm_check'))

warns_check_handler = CallbackQueryHandler(
    handle_warns_check,
    filters.regex('warns_me')
)

contact_me_handler = CallbackQueryHandler(
    handle_contact_me,
    filters.regex('contact_me')
)

about_me_handler = CallbackQueryHandler(
    handle_about_me,
    filters.regex('about_me')
)

deny_user_handler = CallbackQueryHandler(
    handle_deny_user,
    filters.regex('deny_user')
)

approve_user_handler = CallbackQueryHandler(
    handle_approve_user,
    filters.regex('approve_user')
)

unblock_user_handler = CallbackQueryHandler(
    handle_unblock_user,
    filters.regex('unblock_user')
)
