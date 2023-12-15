
from telebot import TeleBot
from time import sleep
from logging import info, warning
from modules.lib.jsonutils import JsonUtils
from modules.lib.validation import Validation
from modules.lib.messages import MessageData
from modules.lib.dataprocess import DataProcess


class BotinPACTA:
    """Teste de uma abstração maior"""

    def __init__(self, credentials:object, users:object) -> None:
        """Objeto que representa o bot do telegram da inPACTA."""
        self.token, self.name_bot, self.admin_, self.absolutepath, self.cachedirectory = credentials.get_credentials()
        self.bot = TeleBot(self.token)
        self.users = users
        self.admin = [user for user in self.users.list_users if user.privileges == 'admin']
        self.user_ids = [user.id for user in self.users.list_users]
        self.user_names = [user.name for user in self.users.list_users]
        self.time_sleep = 0.2
        self.bot.send_message(self.admin[0].id, "Bot iniciado com sucesso!")

    def get_started(self) -> None:
        """Método que recebe o comando "/start"."""
        @self.bot.message_handler(commands=['start'])
        def send_welcome(message) -> None:
            MessageData.get_data(message, self.bot, self.time_sleep, self.admin)
            data = """Olá, aqui é o Bot da Inpacta, para ver os comandos disponíveis digite:\n  /Ajuda """
            sleep(self.time_sleep)
            self.bot.reply_to(message, data)
    
    def get_prompt(self) -> None:
        """Método que lida com o prompt do bot."""
        @self.bot.message_handler(func=Validation.is_valid_input)
        def send_prompt_text(message) -> None:
            MessageData.get_data(message, self.bot, self.time_sleep, self.admin)
            self.bot.reply_to(message, Validation.is_valid_text(message.text))
            
    def get_help(self) -> None:
        """Método que recebe o comando "/ajuda" ou "ajuda"."""
        @self.bot.message_handler(func=lambda message: "ajuda" in message.text.lower())
        def send_help(message):
            MessageData.get_data(message, self.bot, self.time_sleep, self.admin)
            data = """
            Comandos disponíveis:
            /horarios - Exibe os horários
            /agendar - Agenda um horário
            /bolsistas - Exibe os bolsistas
            /gestores - Exibe os gestores
            /sobre - Exibe informações sobre o bot
            /ajuda - Exibe os comandos disponíveis
            """
            self.bot.reply_to(message, data)

    def get_about(self) -> None:
        """Método que recebe o comando "/sobre"."""
        @self.bot.message_handler(commands=['sobre'])
        def send_sobre(message):
            MessageData.get_data(message, self.bot, self.time_sleep, self.admin)
            self.bot.reply_to(message, """Bot em desenvolvimento pela Inpacta, para mais informações acesse:\n    https://sites.google.com/view/inpacta/""")
        
    def get_schedule(self) -> None:
        """Método que recebe o comando "/agendar"."""
        @self.bot.message_handler(commands=['agendar'])
        def send_agendar(message):
            MessageData.get_data(message, self.bot, self.time_sleep, self.admin)
            self.bot.reply_to(message, """Para agendar um horário, entre com: \n'agendar data horário conteúdo' \n   Exemplo: agendar 01/01 10:00 "encontro com o gestor" """)

    def manage_schedule(self) -> None:
        """Método que lida com o "agendar"."""
        @self.bot.message_handler(func=lambda message: "agendar" in message.text.lower())
        def handle_schedule(message):
            MessageData.get_data(message, self.bot, self.time_sleep, self.admin)
            args = message.text.split()
            print(f" agendar args: {args}")
            if args[0].lower() != "agendar":
                self.bot.reply_to(message, "Formato de mensagem inválido. \nUse: 'agendar 01/01 10:00 encontro com o gestor'")
            else:
                if len(args) < 4:
                    self.bot.reply_to(message, "Formato de mensagem inválido. \nUse: 'agendar 01/01 10:00 encontro com o gestor'")
                    return
                
                day, time, content = args[1], args[2], args[3:]

                if not Validation.is_valid_date(day):
                    self.bot.reply_to(message, "Data inválida. Use o formato dd/mm.")
                    return
                
                if not Validation.is_valid_time(time):
                    self.bot.reply_to(message, "Horário inválido. Use o formato hh:mm.")
                    return
                dataprocess = DataProcess()
                data = dataprocess.get_data_from_sheets(day, time)
                if data in ["Não tem bolsista neste horário.", "Horário inválido.", "Dia inválido.", "Final de semana, não tem horário.", "Não foi possível acessar a planilha. Tente novamente mais tarde."]:
                    self.bot.reply_to(message, data)
                    return
                
                else:
                    recipient = message.chat.id
                    content = ' '.join(content)
                    if  not message.from_user.last_name is None :
                        name = message.from_user.first_name
                    if not message.from_user.last_name is None:
                        name = message.from_user.first_name + ' ' + message.from_user.last_name
                    if not message.from_user.username is None:
                        name = message.from_user.username
                    else:
                        name = message.chat.id
                    user_data = {'recipient': recipient, 'name': name, 'content': content, 'day_and_time': f'{day} {time}'}
                    response = f'Entrei em contato com o(s) bolsista(s) e aguardando a resposta.'
                    MessageData.manage_delivery(data, user_data, self.time_sleep, self.cachedirectory, self.user_names, self.user_ids, self.bot)
                    sleep(self.time_sleep)
                    self.bot.reply_to(message, response)

    def get_especific_chats(self) -> None:
        """Método que lida com as respostas dos bolsistas."""
        @self.bot.message_handler(func=lambda message: "sim" in message.text.lower() or "não" in message.text.lower() or "nao" in message.text.lower())
        def handle_specific_chats(message) -> None:
            """Função para gerenciar as mensagens específicas."""
            MessageData.get_data(message, self.bot, self.time_sleep, self.admin)
            if "sim" in message.text.lower():
                msg = "Ok, aguarde um momento..."
                self.bot.reply_to(message, msg)
                data = JsonUtils.read_and_remove_first_item(self.cachedirectory)
                if isinstance(data, str):
                    self.bot.reply_to(message, data)
                    return
                recipient = data[1]['recipient']
                msg = f'Olá {data[1]["name"]}, {message.from_user.first_name} {message.from_user.last_name} aceitou o seu pedido. \nConteúdo: {data[1]["content"]}'
                self.bot.send_message(recipient, msg)
                sleep(self.time_sleep)
                self.bot.reply_to(message, "Mensagem enviada com sucesso!")
            elif "não" in message.text.lower() or "nao" in message.text.lower():
                msg = "Ok, aguarde um momento..."
                self.bot.reply_to(message, msg)
                sleep(self.time_sleep)
                data = JsonUtils.read_and_remove_first_item(self.cachedirectory)
                if isinstance(data, str):
                    self.bot.reply_to(message, data)
                    return
                recipient = data[1]['recipient']
                msg = f'Olá {data[1]["name"]}, {message.from_user.first_name} {message.from_user.last_name} não aceitou o seu pedido. \nConteúdo: {data[1]["content"]}'
                self.bot.send_message(recipient, msg)
                sleep(self.time_sleep)
                self.bot.reply_to(message, "Mensagem enviada com sucesso!")

    def get_gestores(self) -> None:
        """Método que lida com o "/gestores"."""
        @self.bot.message_handler(commands=['gestores'])
        def send_gestores(message):
            MessageData.get_data(message, self.bot, self.time_sleep, self.admin)
            gestores = sorted(DataProcess().get_gestores())
            mensagem = "Os gestores atuais são:\n" + "\n".join(f"      {i+1}. {nome}" for i, nome in enumerate(gestores))
            self.bot.reply_to(message, mensagem)

    def get_bolsistas(self) -> None:
        """Método que lida com o "/bolsistas"."""
        @self.bot.message_handler(commands=['bolsistas'])
        def send_bolsistas(message):
            MessageData.get_data(message, self.bot, self.time_sleep, self.admin)
            bolsistas = sorted(DataProcess().get_bolsistas())
            mensagem = "Os bolsistas atuais são:\n" + "\n".join(f"      {i+1}. {nome}" for i, nome in enumerate(bolsistas))
            self.bot.reply_to(message, mensagem)

    def get_horarios(self) -> None:
        """Método que lida com o "/horarios"."""
        @self.bot.message_handler(commands=['horarios'])
        def send_horarios(message):
            MessageData.get_data(message, self.bot, self.time_sleep, self.admin)
            data = """
            Os horários disponíveis são: \n   - matutino \n   - vespertino \n   - noturno \nExemplo: \n     "horarios matutino" \nExibe o horário do
            "horario matutino" """
            self.bot.reply_to(message, data)

    def handle_horarios(self) -> None:
        """Método que lida com o "horários"."""
        @self.bot.message_handler(func=lambda message: 
                     "horario" in message.text.lower() 
                     or "horário" in message.text.lower() 
                     or "horários" in message.text.lower() 
                     or "horarios" in message.text.lower() 
                     and "/" not in message.text.lower()
                     )
        def send_horarios_matutino(message) -> None:
            MessageData.get_data(message, self.bot, self.time_sleep, self.admin)
            chatIDpessoa=message.chat.id
            self.bot.reply_to(message, "Aguarde um momento...")
            args = message.text.split()
            print(f" horarios args: {args}")

            if len(args) < 2:
                msg = "Formato de mensagem inválido! \nPor favor, use: \n   'horarios matutino'"
                sleep(self.time_sleep)
                self.bot.reply_to(message, msg)
                return

            if args[1].lower() == "matutino":
                self.bot.send_photo(chatIDpessoa, open(f'{self.absolutepath}modules/images/horarios-matutino.png', 'rb'))

            if args[1].lower() == "vespertino":
                self.bot.send_photo(chatIDpessoa, open(f'{self.absolutepath}modules/images/horarios-vespertino.png', 'rb'))
            
            if args[1].lower() == "noturno":
                self.bot.send_photo(chatIDpessoa, open(f'{self.absolutepath}modules/images/horarios-noturno.png', 'rb'))
            
            if args[1].lower() not in ["matutino", "vespertino", "noturno"]:
                msg = "Horário inválido"
                sleep(self.time_sleep)
                self.bot.reply_to(message, msg)
    
    def run(self) -> None:
        """Método que inicia o bot."""
        self.get_started()
        self.get_prompt()
        self.get_help()
        self.get_about()
        self.get_schedule()
        self.manage_schedule()
        self.get_especific_chats()
        self.get_gestores()
        self.get_bolsistas()
        self.get_horarios()
        self.handle_horarios()
        info("Bot iniciado com sucesso!")
        self.bot.polling()
        self.bot.send_message(self.admin[0].id, "Bot finalizado com sucesso!")
        info("Bot finalizado com sucesso!")

    def kill(self) -> None:
        """Método que finaliza o bot."""
        self.bot.stop_polling()

    def reboot(self) -> None:
        """Método que reinicia o bot."""
        self.kill()
        self.run()

    def bot_helper(self, message) -> None:
        """Método que lida com o comando "/bot"."""
        bot = TeleBot(self.token)
        bot.send_message(self.admin[0].id, message)