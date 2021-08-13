from dotenv import load_dotenv
import os

load_dotenv()
api_id = os.getenv('api_id')
api_hash = os.getenv('api_hash')

log_group = int(os.getenv('log_group'))
bot_token = os.getenv('bot_token')
bot_id = int(os.getenv('bot_id'))
bot_username = os.getenv('bot_username')
owner_id = int(os.getenv('owner_id'))
warn_limit = int(os.getenv('warn_limit'))
pm_log_group = int(os.getenv('pm_log_group'))
