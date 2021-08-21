from .db import allowed_groups
from pyrogram import filters

allowed_group_filter = filters.create(
    lambda _, __, update: update.chat.id in allowed_groups)


def is_welcome_enabled(_, __, update):
    try:
        group = allowed_groups.get(update.chat.id)
        return group.enable_welcome
    except Exception:
        return False


def is_leave_enabled(_, __, update):
    try:
        group = allowed_groups.get(update.chat.id)
        return group.enable_leave
    except Exception:
        return False


def is_service_removal_enabled(_, __, update):
    try:
        group = allowed_groups.get(update.chat.id)
        return group.remove_service_msg
    except Exception:
        return False


welcome_enabled_filter = filters.create(is_welcome_enabled)
leave_enabled_filter = filters.create(is_leave_enabled)
service_removal_filter = filters.create(is_service_removal_enabled)
