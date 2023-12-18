
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

def main():
    try:
        sleep(0.5)
        bot.run()
    except KeyboardInterrupt:
        bot.kill()
    except Exception as e:
        warning(f"Error: {e}")
        sleep(0.5)
        bot.bot_helper(f"Ocorreu um erro {e}, o bot foi reiniciado!")  
        main()

if __name__ == "__main__":
    main()
        

