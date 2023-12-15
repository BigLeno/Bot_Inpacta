
from logging import basicConfig, warning, INFO
from dotenv import load_dotenv
from time import sleep

load_dotenv()
basicConfig(level=INFO)

from modules.lib.credentials import Credentials
from modules.lib.users import Users

from modules.lib.telegrambot import BotinPACTA


credentials = Credentials()
users = Users()

bot = BotinPACTA(credentials, users)

while True:
    try:
        bot.run()
    except KeyboardInterrupt:
        bot.kill()
        break
    except Exception as e:
        warning(f"Error: {e}")
        bot.bot_helper(f"Ocorreu um erro {e}, o bot foi reiniciado!")  
        bot.reboot()

