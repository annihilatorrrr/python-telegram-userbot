from .init import userbot, bot
from pyrogram import idle
from logzero import logger

logger.info('Initializing userbot')
userbot.start()
logger.info('Initializing bot')
bot.start()

idle()

userbot.stop()
bot.stop()
