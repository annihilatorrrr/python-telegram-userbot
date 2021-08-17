from .db import allowed_groups
from pyrogram import filters

allowed_group_filter = filters.create(
    lambda _, __, update: update.chat.id in allowed_groups)
