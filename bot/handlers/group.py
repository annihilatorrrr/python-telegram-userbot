from pyrogram import filters
from pyrogram.handlers import MessageHandler
from ..db import allowed_groups, Group
from ..filters import (allowed_group_filter,
                       welcome_enabled_filter,
                       leave_enabled_filter,
                       service_removal_filter)
from .. import utils
from logzero import logger


def handle_service_message(client, msg):
    msg.delete()
    msg.continue_propagation()


def handle_join(client, msg):
    group = allowed_groups.get(msg.chat.id)
    template = group.welcome_text
    texts = []
    for user in msg.new_chat_members:
        texts.append(
            template.format(user=user.mention)
        )
    for text in texts:
        try:
            client.send_message(msg.chat.id, text, parse_mode="HTML")
        except Exception as e:
            logger.error(str(e))


def handle_chat_id(client, msg):
    msg.edit_text(msg.chat.id)


def handle_leave(client, msg):
    group = allowed_groups.get(msg.chat.id)
    template = group.exit_text
    text = template.format(user=msg.left_chat_member.mention)
    client.send_message(msg.chat.id, text, parse_mode="HTML")


def handle_allow_group(client, msg):
    q = Group.select().where(
        Group.group_id == msg.chat.id
    )

    if q.count():
        group = q.get()
        group.enabled = True
        group.save()
    else:
        group = Group(group_id=msg.chat.id,
                      enabled=True,
                      enable_welcome=False,
                      enable_leave=False,
                      remove_service_msg=False)
        group.save()

    allowed_groups.add(msg.chat.id, group, replace=True)
    msg.edit_text('Group has been enabled.')


def handle_disallow_group(client, msg):
    q = Group.select().where(
        Group.group_id == msg.chat.id
    )

    if not q.count():
        msg.delete()
        return

    try:
        group = q.get()
        group.enabled = False
        group.save()
        allowed_groups.remove(msg.chat.id)
    except Exception as e:
        print(str(e))

    msg.edit_text('Group has been disabled')


def handle_enable_welcome(client, msg):
    group_id = msg.chat.id
    group = Group.select().where(
        Group.group_id == group_id
    ).get()

    group.enable_welcome = True
    group.save()
    allowed_groups.add(group_id, group, replace=True)
    msg.edit('Welcome messages enabled.')


def handle_disable_welcome(client, msg):
    group_id = msg.chat.id
    group = Group.select().where(
        Group.group_id == group_id
    ).get()

    group.enable_welcome = False
    group.save()
    allowed_groups.add(group_id, group, replace=True)
    msg.edit('Welcome messages disabled.')


def handle_enable_service(client, msg):
    group_id = msg.chat.id
    group = Group.select().where(
        Group.group_id == group_id
    ).get()

    group.remove_service_msg = True
    group.save()
    allowed_groups.add(group_id, group, replace=True)
    msg.edit('Service message removal enabled')


def handle_disable_service(client, msg):
    group_id = msg.chat.id
    group = Group.select().where(
        Group.group_id == group_id
    ).get()

    group.remove_service_msg = False
    group.save()
    allowed_groups.add(group_id, group, replace=True)
    msg.edit('Service message removal disabled')


def handle_enable_leave(client, msg):
    group_id = msg.chat.id
    group = Group.select().where(
        Group.group_id == group_id
    ).get()

    group.enable_leave = True
    group.save()
    allowed_groups.add(group_id, group, replace=True)
    msg.edit('Leave messages enabled')


def handle_disable_leave(client, msg):
    group_id = msg.chat.id
    group = Group.select().where(
        Group.group_id == group_id
    ).get()

    group.enable_leave = False
    group.save()
    allowed_groups.add(group_id, group, replace=True)
    msg.edit('Leave messages disabled')


def handle_configure_greetings(client, msg):
    notice = None
    group_id = msg.chat.id
    command = msg.command[0]
    try:
        text = msg.text.split(' ', 1)[1]
    except IndexError:
        msg.delete()
        return False

    group = Group.select().where(
        Group.group_id == group_id
    ).get()

    if command == 'welcome_msg':
        group.welcome_text = text
        notice = 'Welcome message'
    elif command == 'leave_msg':
        group.exit_text = text
        notice = 'Exit message'

    group.save()
    allowed_groups.add(group_id, group, replace=True)
    msg.edit_text(
        f'{notice} has been updated'
    )


def handle_group_info(client, msg):
    group = allowed_groups.get(msg.chat.id)
    text = utils.process_group_info(group)
    msg.edit_text(text, parse_mode="HTML")


"""
    You will notice that certain handlers are not using ~filters.private
    This is because allowed_group_filter will also check if the message is
    a group chat.
"""

service_msg_handler = MessageHandler(
    handle_service_message,
    (
        (filters.service & ~filters.me) & allowed_group_filter
        & service_removal_filter
    )
)

new_member_handler = MessageHandler(
    handle_join,
    (
        (filters.new_chat_members & ~filters.me) & allowed_group_filter
        & welcome_enabled_filter
    )
)

member_leave_handler = MessageHandler(
    handle_leave,
    (
        (filters.left_chat_member & ~filters.me) & allowed_group_filter
        & leave_enabled_filter
    )
)

get_chatid_handler = MessageHandler(
    handle_chat_id,
    filters.command('chat_id', '.') & filters.me
)

allow_group_handler = MessageHandler(
    handle_allow_group,
    (filters.command('enable_group', '.') & filters.me) & ~filters.private
)

disallow_group_handler = MessageHandler(
    handle_disallow_group,
    (filters.command('disable_group', '.') & filters.me) & ~filters.private
)

enable_welcome_handler = MessageHandler(
    handle_enable_welcome,
    (
        filters.command('enable_welcome', '.') & filters.me
    ) & allowed_group_filter
)

disable_welcome_handler = MessageHandler(
    handle_disable_welcome,
    (
        filters.command('disable_welcome', '.') & filters.me
    ) & allowed_group_filter
)


enable_leave_handler = MessageHandler(
    handle_enable_leave,
    (
        filters.command('enable_leave', '.') & filters.me
    ) & allowed_group_filter
)

disable_leave_handler = MessageHandler(
    handle_disable_leave,
    (
        filters.command('disable_leave', '.') & filters.me
    ) & allowed_group_filter
)

enable_service_handler = MessageHandler(
    handle_enable_service,
    (
        filters.command('enable_service', '.') & filters.me
    ) & allowed_group_filter
)

disable_service_handler = MessageHandler(
    handle_disable_service,
    (
        filters.command('disable_service', '.') & filters.me
    ) & allowed_group_filter
)

configure_greetings_handler = MessageHandler(
    handle_configure_greetings,
    (
        filters.command(['leave_msg', 'welcome_msg'], '.') & filters.me
    ) & allowed_group_filter
)

group_info_handler = MessageHandler(
    handle_group_info,
    ((filters.command('group_info', '.') & filters.me) & allowed_group_filter)
)
