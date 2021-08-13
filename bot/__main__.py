from .init import userbot, bot
from pyrogram import idle
from logzero import logger
from .handlers import (filters as message_filters,
                       group,
                       urbandict,
                       users,
                       bot_misc)

logger.info('Initializing userbot handlers')
userbot.add_handler(message_filters.add_filter_handler)
userbot.add_handler(message_filters.rm_filter_handler)
userbot.add_handler(message_filters.process_filter_handler, group=-1)
userbot.add_handler(group.get_chatid_handler)
userbot.add_handler(group.new_member_handler)
userbot.add_handler(urbandict.urbandict_handler)
userbot.add_handler(users.pm_handler, group=-1)

logger.info('Initializing bot handlers')
bot.add_handler(bot_misc.pm_check_handler)
bot.add_handler(bot_misc.warns_check_handler)
bot.add_handler(bot_misc.contact_me_handler)
bot.add_handler(bot_misc.deny_user_handler)
bot.add_handler(bot_misc.unblock_user_handler)


userbot.start()
bot.start()

idle()

userbot.stop()
bot.stop()
