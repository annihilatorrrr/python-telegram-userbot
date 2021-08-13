from pyrogram import Client
from .config import (api_id,
                     api_hash,
                     bot_token)

userbot = Client('../user', api_id, api_hash)
bot = Client(bot_token, api_id, api_hash)
