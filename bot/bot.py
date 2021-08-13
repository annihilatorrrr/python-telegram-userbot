from pyrogram import Client, idle
from logzero import logger
from config import api_id, api_hash, bot_token
from handlers import bot_misc


def run_bot():
    logger.info('Bot initializd')
    bot = Client(bot_token, api_id, api_hash)
    bot.add_handler(bot_misc.start_handler)
    bot.run()
    idle()


if __name__ == '__main__':
    run_bot()
