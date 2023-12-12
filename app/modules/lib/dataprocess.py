
from datetime import datetime, timedelta
from logging import info, warning

import pandas as pd

from modules.lib.googleservices import GoogleSheets

# Para rodar localmente
# from googleservices import GoogleSheets

class DataProcess:
    def __init__(self) -> None:
        """Inicializa as variáveis necessárias para o processamento dos dados."""
        self.day_to_index = { 0 :'Segunda', 1:'Terça', 2:'Quarta', 3:'Quinta', 4:'Sexta', 5:'Sábado', 6:'Domingo'}
        self.allowed_times = ['M12', 'M34', 'M56', 'T12', 'T34', 'T56', 'N12', 'N34']
        self.time_to_interval = {
            'M12': range(7, 8),'M34': range(9, 10),'M56': range(11, 12),
            'T12': range(13, 14),'T34': range(15, 16),'T56': range(17, 18),
            'N12': range(19, 20),'N34': range(21, 22)
            }
        self.textstamps = ["hoje", "amanhã",'%d/%m/%Y', '%H:%M']

    def get_day(self, user_input:str) -> int or None:
        """Retorna o dia da semana correspondente ao input do usuário."""
        if user_input.lower() == self.textstamps[0]:
            return datetime.now().date().weekday()
        elif user_input.lower() == self.textstamps[1]:
            return (datetime.now().date() + timedelta(days=1)).weekday()

        try:
            if user_input[-4:].isdigit():
                return datetime.strptime(user_input, self.textstamps[2]).date()
            else:
                return datetime.strptime(user_input + '/' + str(datetime.now().year), self.textstamps[2]).date().weekday()

        except ValueError:
            print("Não foi possível entender a data. Por favor, use o formato DD/MM ou DD/MM/AAAA.")
            return None

        
    def get_time_interval(self, time) -> str:
        """Retorna o intervalo de tempo correspondente ao input do usuário."""

        if (time.lower()).capitalize() in self.allowed_times:
            return time
        else:
            if time.isdigit():
                time += ':00'
            elif 'h' in time or 'H' in time:
                time = time.replace('h', ':').replace('H', ':')
                if len(time) == 3:  # Se não houver minutos, adiciona ':00'
                    time += '00'

            hour, minute = datetime.strptime(time, self.textstamps[3]).time().hour, datetime.strptime(time, self.textstamps[3]).time().minute

            for interval, hours in self.time_to_interval.items():
                if hour in hours:
                    return interval if minute < 50 else next((i for i in self.time_to_interval if i > interval), None)
                    
        return min(self.time_to_interval.keys(), key=lambda interval: abs(hour - self.time_to_interval[interval][0]))

    def get_data_from_sheets(self, day, time):

        sheets = GoogleSheets()

        result = sheets.get_sheets()

        if not result:
            return "Não foi possível acessar a planilha. Tente novamente mais tarde."

        day_index = self.get_day(day) + 1
        formated_time = self.get_time_interval(time)

        for row in result:
            if all(item not in row for item in ['M12','N34','DIAS DA SEMANA']) and row and day_index not in [6, 7]:
                if (row[0] == formated_time and 
                    0 < day_index < len(row) and 
                    formated_time in self.allowed_times and 
                    row[day_index] != 'X'):

                    bolsistas = [bolsista.strip() for bolsista in row[day_index].split('/')]

                    if len(bolsistas) == 1:
                        info("Bolsista encontrado!")
                        return bolsistas[0]
                    elif len(bolsistas) == 2:
                        info("Dois bolsistas encontrados!")
                        return bolsistas[0], bolsistas[1]
                    elif len(bolsistas) == 3:
                        info("Três bolsistas encontrados!")
                        return bolsistas[0], bolsistas[1], bolsistas[2]
                    
                elif (row[0] == formated_time and 
                    row[day_index] == 'X' and 
                    formated_time in self.allowed_times and 
                    0 < day_index < len(row)):
                    
                    info("Horário vazio")
                    return "Não tem bolsista neste horário."
                
                elif formated_time not in self.allowed_times and 0 < day_index < len(row):
                    warning("Horário inválido.")
                    return "Horário inválido."
                
                elif not (0 < day_index < len(row)):
                    warning("Dia inválido.")
                    return "Dia inválido."
                
                elif day_index in [6, 7]:
                    warning("Final de semana, não tem horário.")
                    return "Final de semana, não tem horário."
                
    def get_bolsistas(self) -> list or str:
        """Retorna a lista de bolsistas."""

        sheets_matutino = GoogleSheets(sample_range_name='Página1!B3:G9')
        sheets_vespertino = GoogleSheets(sample_range_name='Página1!B12:G18')
        sheets_noturno = GoogleSheets(sample_range_name='Página1!B21:G25')
        
        result_matutino = pd.DataFrame(sheets_matutino.get_sheets())
        result_vespertino = pd.DataFrame(sheets_vespertino.get_sheets())
        result_noturno = pd.DataFrame(sheets_noturno.get_sheets())

        if result_matutino.empty or result_vespertino.empty or result_noturno.empty:
            return "Não foi possível acessar a planilha. Tente novamente mais tarde."
        
        remover = ['HORÁRIOS - manhã', 'Segunda-feira', 'Terça-Feira', 
                   'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 
                   'Sábado', 'Domingo', 'HORÁRIOS - tarde', 'HORÁRIOS - noite', 
                   'Bolsistas', 'Bolsistas:', 'X', None, 'M12', 'M34', 'M56', 
                   'T12', 'T34', 'T56', 'N12', 'N34', 'None', 'x']

        df = pd.concat([result_matutino, result_vespertino, result_noturno])
        serie = df.values.flatten()

        serie = df.values.flatten()

        nomes = list(set([nome.strip() for sublist in serie for nome in str(sublist).split('/') if nome not in remover]))

        return nomes

    def get_gestores(self):
        """Retorna a lista de gestores."""
        sheets = GoogleSheets(sample_range_name='Página1!B28:G31')

        result = sheets.get_sheets()

        if not result:
            return "Não foi possível acessar a planilha. Tente novamente mais tarde."

        result = [gestor for sublist in result for gestor in sublist]

        return result


# if __name__ == "__main__":
#   day = input("Digite o dia: ")
#   time = input("Digite a hora: ")
#   print(get_data_from_sheets(day, time))
    