from .init import userbot, bot
from pyrogram import idle
from logzero import logger
from .handlers import (filters as message_filters,
                       group,
                       urbandict,
                       users,
                       bot_misc)
from .utils import (load_allowed_users,
                    load_allowed_groups)


logger.info('Loading user info to cache')
load_allowed_users()
logger.info('Loading allowed groups into cache')
load_allowed_groups()


logger.info('Attaching userbot handlers')

"""
    Handlers for adding/removing and processing filters
"""
userbot.add_handler(message_filters.add_filter_handler)
userbot.add_handler(message_filters.rm_filter_handler)
userbot.add_handler(message_filters.process_filter_handler, group=-0)

"""
    Handlers for handling groups.
    Grabbing chat id
    enable/disable group
    enable/disable welcome messages
    enable/disable removing of service messages
"""
userbot.add_handler(group.get_chatid_handler)
userbot.add_handler(group.service_msg_handler)
userbot.add_handler(group.new_member_handler)
userbot.add_handler(group.member_leave_handler)
userbot.add_handler(group.allow_group_handler)
userbot.add_handler(group.disallow_group_handler)
userbot.add_handler(group.enable_welcome_handler)
userbot.add_handler(group.disable_welcome_handler)
userbot.add_handler(group.enable_service_handler)
userbot.add_handler(group.disable_service_handler)
userbot.add_handler(group.enable_leave_handler)
userbot.add_handler(group.disable_leave_handler)
userbot.add_handler(group.configure_greetings_handler)
userbot.add_handler(group.group_info_handler)

userbot.add_handler(urbandict.urbandict_handler)

"""
    PM Handlers
    Allow/block user
    PMSecurity
"""
userbot.add_handler(users.pm_handler, group=-1)
userbot.add_handler(users.approve_user_handler)
userbot.add_handler(users.block_user_handler)

logger.info('Attaching bot handlers')
bot.add_handler(bot_misc.pm_check_handler)
bot.add_handler(bot_misc.inline_deny_handler)
bot.add_handler(bot_misc.warns_check_handler)
bot.add_handler(bot_misc.contact_me_handler)
bot.add_handler(bot_misc.about_me_handler)
bot.add_handler(bot_misc.misc_handler)
bot.add_handler(bot_misc.deny_user_handler)
bot.add_handler(bot_misc.approve_user_handler)
bot.add_handler(bot_misc.unblock_user_handler)


# userbot.start()
# bot.start()

# idle()

# userbot.stop()
# bot.stop()

if __name__ == '__main__':
    try:
        userbot.start()
        bot.start()
        idle()
    except KeyboardInterrupt:
        print('Exitting...')
        userbot.stop()
        bot.stop()
