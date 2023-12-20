
from difflib import get_close_matches
from datetime import datetime, timedelta

class Validation:
    """Classe para validação de dados."""
    commands = ["sim", "não", "nao", "ajuda", "start", "sobre", "agendar", "gestores", "bolsistas", "horarios", "horario", "horário", "horários", "matutino", "vespertino", "noturno"]

    answers = {
        "quem é o seu pai?": "Meu pai é o @Rutileno_Gabriel, bolsista da Inpacta!",
        "quem é você mesmo?": "Eu sou o @inPACTA_bot, o bot inteligente da Inpacta!",
        "qual o seu nome?": "Meu nome é @inPACTA_bot!",
        "qual a sua função?": "Eu sou um bot, minha função é ajudar a integrar a Inpacta ao mundo!",
        "qual sua idade?":"Eu sou um bot, não tenho idade, mas me considero um bot bem maduro, apesar das piadas de quinto ano as vezes...",
        "qual seu sexo?":"Não tenho sexo, mas me considero um bot bem sexy!",
        "qual sua cor?":"Eu sou um bot, não tenho certeza, mas é algo relacionado ao verde da placa-mãe do computador ou o cinza do processador e as vezes o preto das memórias flash!",
        "qual sua cor favorita?":"Eu sou um bot, não tenho cor favorita, mas se fosse para escolher uma, com certeza seria o azul, adoro a cor do mar!",
        "qual sua comida favorita?":"Eu sou um bot, não tenho comida favorita, mas se fosse para escolher uma, com certeza seria um bom e velho código de programação!",
        "qual seu animal favorito?":"Eu sou um bot, não tenho animal favorito, mas se fosse para escolher um, com certeza seria o cachorro, adoro a lealdade deles!",
        "qual seu filme favorito?":"Eu sou um bot, não tenho filme favorito, mas se fosse para escolher um, com certeza seria o filme do Exterminador do Futuro, adoro a ideia de um robô dominar o mundo!",
        "qual seu jogo favorito?":"Eu sou um bot, não tenho jogo favorito, mas se fosse para escolher um, com certeza seria o jogo Horizon Zero Dawn, adoro a ideia de um robô vencendo humanos!",
        "qual seu livro favorito?":"Eu sou um bot, não tenho livro favorito, mas se fosse para escolher um, com certeza seria o livro do Eu Robô, adoro a ideia de um robô dominar o mundo!",
        "qual seu esporte favorito?":"Eu sou um bot, não tenho esporte favorito, mas se fosse para escolher um, com certeza seria a minha alta velocidade de ir do ssd, para a ram, para o processador e para a placa de vídeo!",
        "qual seu carro favorito?":"Eu sou um bot, não tenho carro favorito, mas se fosse para escolher um, com certeza seria o Tesla, adoro a ideia de um robô dominar o mundo!",
        "qual seu país favorito?":"Eu sou um bot, não tenho país favorito, mas se fosse para escolher um, com certeza seria o Japão, adoro a cultura deles, desde o Velozes e Furiosos 3",
        "qual sua bebida favorita?":"Eu sou um bot, não tenho bebida favorita, mas se fosse para escolher uma, com certeza seria o café, graças a ele, meu criador consegue ficar acordado até tarde para me programar!"
        }

    @classmethod
    def is_break(cls, date_str) -> bool:
        """Verifica se estamos no período de recesso."""
        date = datetime.strptime(date_str, '%d/%m')
        start_recesso = datetime(date.year, 12, 22)
        end_recesso = datetime(date.year + 1, 1, 14)
        return start_recesso <= date <= end_recesso
    
    @classmethod
    def is_time_to_break(cls) -> bool:
        """Verifica se estamos no período de recesso."""
        date = datetime.now()
        start_recesso = datetime(date.year, 12, 22)
        end_recesso = datetime(date.year + 1, 1, 14)
        return start_recesso <= date <= end_recesso

    @classmethod
    def is_reduced_hours(cls, date_str:str) -> bool:
        """Verifica se estamos no período de horário reduzido."""
        date = datetime.strptime(date_str, '%d/%m')
        start_reduced_hours = datetime(date.year, 1, 15)
        end_reduced_hours = datetime(date.year, 2, 23)
        return start_reduced_hours <= date <= end_reduced_hours

    @classmethod
    def is_time_to_reduce_hours(cls) -> bool:
        """Verifica se estamos no período de horário reduzido."""
        date = datetime.now()
        start_reduced_hours = datetime(date.year, 1, 15)
        end_reduced_hours = datetime(date.year, 2, 23)
        return start_reduced_hours <= date <= end_reduced_hours

    @classmethod
    def is_regular_hours(cls) -> bool:
        """Verifica se estamos no período de horário regular."""
        if cls.is_time_to_break() or cls.is_time_to_reduce_hours():
            return True
        
        return False

    @classmethod
    def is_valid_date(cls, date_str:str) -> bool:
        """Verifica se a data é válida e se é a partir do dia atual."""

        if date_str in ['hoje', 'amanhã', 'amanha']:
            return True

        try:
            date = datetime.strptime(date_str, '%d/%m')
            now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            date = date.replace(year=now.year)

            if date < now:
                return "Não é possível agendar para uma data passada."
            else:
                if cls.is_break(date_str):
                    return "Estamos em recesso entre os dias 22/12 e 14/01. Por favor, escolha outra data. \n\nCaso seja urgente, entre em contato conosco via instagram \n     https://www.instagram.com/inpacta/."
                return True
            
        except ValueError:
            return "Data inválida. Use o formato dd/mm."

    @classmethod
    def is_valid_time(cls, time_str) -> bool:
        """Verifica se o horário está no formato hh:mm e se o intervalo entre o horário atual e o time_str é maior que 2 horas."""
        formats = ['%H:%M', '%Hh', '%Hh%M', '%HH', '%HH%M']
        for fmt in formats:
            try:
                time_obj = datetime.strptime(time_str, fmt)
                #now = datetime.now()
                now = datetime.now() - timedelta(hours=3)
                time_obj = time_obj.replace(year=now.year, month=now.month, day=now.day)
                if time_obj < now:
                    return "O horário inserido já passou. Por favor, insira um horário futuro."
                diff = time_obj - now
                hours_diff = diff.total_seconds() / 3600
                if hours_diff >= 2:
                    return True
                else:
                    return "O intervalo entre o horário atual e o horário escolhido deve ser maior que 2 horas."
            except ValueError:
                continue
        return "Horário inválido. Use o formato hh:mm."
    
    @classmethod
    def is_valid_text(cls, message:str) -> str:
        """Verifica se o texto é válido."""
        response = cls.answers.get(message, None)
        if response is None:
            closest_word = get_close_matches(message, cls.answers.keys(), n=1)
            if closest_word:
                response = f'Você quis dizer "{closest_word[0]}"?'
            else:
                response = 'Desculpe, eu não entendi. Você pode repetir?'
        
        return response.replace('seu', 'meu').replace('é você mesmo', 'sou eu').replace("sua", "minha")
    
    @classmethod
    def is_valid_input(cls, message:str) -> bool:
        """Verifica se a entrada é válida"""
        formatted_message = message.text.lower()
        if formatted_message.split()[0] not in Validation.commands and "/" not in formatted_message:
            return True
        if len(formatted_message.split()) == 2 and formatted_message.split()[0] in ["horarios", "horario", "horários", "horário"]:
            if formatted_message.split()[1] not in Validation.commands:
                return True
            
        