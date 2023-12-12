
from datetime import datetime, timedelta
from logging import info, warning

from modules.lib.googleservices import get_sheets

# Para rodar localmente
# from googleservices import get_sheets

# Mapeia dias da semana para índices
day_to_index = { 0 :'Segunda', 1:'Terça', 2:'Quarta', 3:'Quinta', 4:'Sexta', 5:'Sábado', 6:'Domingo'}

# Lista de horários permitidos
allowed_times = ['M12', 'M34', 'M56', 'T12', 'T34', 'T56', 'N12', 'N34']

# Mapeia horários para intervalos de tempo
time_to_interval = {
    'M12': range(7, 8),  # 7:00-8:50
    'M34': range(9, 10),  # 9:05-10:55
    'M56': range(11, 12),  # 11:10-13:00
    'T12': range(13, 14),  # 14:00-15:50
    'T34': range(15, 16),  # 16:05-17:55
    'T56': range(17, 18),  # 18:10-20:00
    'N12': range(19, 20),  # 20:00-21:50
    'N34': range(21, 22)  # 22:05-23:55
}

def get_day(user_input:str) -> int or None:
    """Retorna o dia da semana correspondente ao input do usuário."""
    if user_input.lower() == "hoje":
        return datetime.now().date().weekday()
    elif user_input.lower() == "amanhã":
        return (datetime.now().date() + timedelta(days=1)).weekday()

    try:
        if user_input[-4:].isdigit():
            return datetime.strptime(user_input, '%d/%m/%Y').date()
        else:
            return datetime.strptime(user_input + '/' + str(datetime.now().year), '%d/%m/%Y').date().weekday()

    except ValueError:
        print("Não foi possível entender a data. Por favor, use o formato DD/MM ou DD/MM/AAAA.")
        return None

    
def get_time_interval(time) -> str:
    """Retorna o intervalo de tempo correspondente ao input do usuário."""

    if (time.lower()).capitalize() in allowed_times:
        return time
    else:
        if time.isdigit():
            time += ':00'
        elif 'h' in time or 'H' in time:
            time = time.replace('h', ':').replace('H', ':')
            if len(time) == 3:  # Se não houver minutos, adiciona ':00'
                time += '00'

        hour, minute = datetime.strptime(time, '%H:%M').time().hour, datetime.strptime(time, '%H:%M').time().minute

        for interval, hours in time_to_interval.items():
            if hour in hours:
                return interval if minute < 50 else next((i for i in time_to_interval if i > interval), None)
                
    return min(time_to_interval.keys(), key=lambda interval: abs(hour - time_to_interval[interval][0]))

def get_data_from_sheets(day, time):

    result = get_sheets()

    if not result:
      return "Não foi possível acessar a planilha. Tente novamente mais tarde."

    day_index = get_day(day) + 1
    formated_time = get_time_interval(time)

    for row in result:
        if all(item not in row for item in ['M12','N34','DIAS DA SEMANA']) and row and day_index not in [6, 7]:
          if (row[0] == formated_time and 
            0 < day_index < len(row) and 
            formated_time in allowed_times and 
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
              formated_time in allowed_times and 
              0 < day_index < len(row)):
            
            info("Horário vazio")
            return "Não tem bolsista neste horário."
          
          elif formated_time not in allowed_times and 0 < day_index < len(row):
            warning("Horário inválido.")
            return "Horário inválido."
          
          elif not (0 < day_index < len(row)):
            warning("Dia inválido.")
            return "Dia inválido."
          
        elif day_index in [6, 7]:
            warning("Final de semana, não tem horário.")
            return "Final de semana, não tem horário."
          

# if __name__ == "__main__":
#   day = input("Digite o dia: ")
#   time = input("Digite a hora: ")
#   print(get_data_from_sheets(day, time))
    