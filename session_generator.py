from pyrogram import Client
from dotenv import load_dotenv
import os

load_dotenv()
api_id = os.getenv('api_id')
api_hash = os.getenv('api_hash')

with Client(":memory", api_id, api_hash) as app:
    print(app.export_session_string())
