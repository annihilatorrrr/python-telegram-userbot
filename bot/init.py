from pyrogram import Client
from .config import api_id, api_hash, session_string, bot_token
from .handlers import (filters as message_filters,
                       group,
                       urbandict,
                       users,
                       bot_misc)

userbot = Client(session_string, api_id, api_hash)
userbot.add_handler(message_filters.add_filter_handler)
userbot.add_handler(message_filters.rm_filter_handler)
userbot.add_handler(message_filters.process_filter_handler, group=-1)
userbot.add_handler(group.get_chatid_handler)
userbot.add_handler(group.new_member_handler)
userbot.add_handler(urbandict.urbandict_handler)
userbot.add_handler(users.pm_handler, group=-1)

bot = Client(bot_token, api_id, api_hash)
bot.add_handler(bot_misc.pm_check_handler)
bot.add_handler(bot_misc.warns_check_handler)
bot.add_handler(bot_misc.contact_me_handler)
