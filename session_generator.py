from pyrogram import Client
from dotenv import load_dotenv
import os
from logzero import logger
import asyncio


load_dotenv()
phone_number = os.getenv('phone_number')
api_id = os.getenv('api_id')
api_hash = os.getenv('api_hash')
bot_token = os.getenv('bot_token')


async def work():
    logger.info('Attempting to login to account')
    client = Client('user', api_id, api_hash, phone_number=phone_number)
    await client.start()
    bot_client = Client('bot', api_id, api_hash, bot_token=bot_token)
    await bot_client.start()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(work())
