
from logging import basicConfig, warning, INFO
from dotenv import load_dotenv

load_dotenv()
basicConfig(level=INFO)

from modules.lib.credentials import Credentials
from modules.lib.users import Users

from modules.lib.telegrambot import BotinPACTA


credentials = Credentials()
users = Users()

bot = BotinPACTA(credentials, users)

try:
    bot.run()
except KeyboardInterrupt:
    bot.kill()
except Exception as e:
    warning(f"Error: {e}")
    bot.reboot()
