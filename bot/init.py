from pyrogram import Client
from .config import (api_id,
                     api_hash,
                     bot_token,
                     phone_number)

userbot = Client('../user', api_id, api_hash, phone_number=phone_number)
bot = Client('../bot', api_id, api_hash, bot_token=bot_token)
