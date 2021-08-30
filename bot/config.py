from dotenv import load_dotenv
import os

load_dotenv()
phone_number = os.getenv('phone_number')
api_id = os.getenv('api_id')
api_hash = os.getenv('api_hash')

log_group = int(os.getenv('log_group'))
bot_token = os.getenv('bot_token')
bot_id = int(os.getenv('bot_id'))
bot_username = os.getenv('bot_username')
owner_id = int(os.getenv('owner_id'))
warn_limit = int(os.getenv('warn_limit'))
pm_log_group = int(os.getenv('pm_log_group'))
pm_photo = 'https://visualdon.uk/wp-content/uploads/2019/04/1.00_00_04_00.Still002.jpg'
about_me = """
Hey friends, i am an about text. :)))
"""
