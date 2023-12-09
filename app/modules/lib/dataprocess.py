
from logging import basicConfig, warning, info, INFO
from datetime import datetime, timedelta

from modules.lib.googleservices import get_sheets

# Para rodar localmente
# from googleservices import get_sheets


# Definindo o nível do log
basicConfig(level=INFO)

# Mapeia dias da semana para índices
day_to_index = {'Segunda': 1, 'Terça': 2, 'Quarta': 3, 'Quinta': 4, 'Sexta': 5}

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

def get_day(day):
    if day.lower() == 'hoje':
        return (datetime.now().weekday())
    elif day.lower() == 'ontem':
        return (datetime.now() - timedelta(days=1)).weekday()
    elif day.lower() == 'amanhã':
        return (datetime.now() + timedelta(days=1)).weekday()
    else:
        return day_to_index.get((day.lower()).capitalize(), -1)
    
def get_time_interval(time):
    if time in allowed_times:
        return time
    else:
        if time.isdigit():
            time = time + ':00'
        elif 'h' in time:
            if '00' not in time and ':' not in time:  # Se não houver minutos, adiciona ':00'
                time = time.replace('h', ':00')
            else: # Se houver minutos, adiciona ':'
                time = time.replace('h', ':')
        time = datetime.strptime(time, '%H:%M').time()
        hour = time.hour
        minute = time.minute
        for interval, hours in time_to_interval.items():
            if hour in hours and minute < 50:  # Considera apenas os primeiros 50 minutos de cada hora
                return interval
            elif hour in hours and minute >= 50:  # Se os minutos estão próximos do final do intervalo
                next_interval = next((i for i in time_to_interval if i > interval), None)  # Encontra o próximo intervalo
                if next_interval:
                    return next_interval
    # Se a hora não corresponder a nenhum intervalo, retorna o intervalo mais próximo
    return min(time_to_interval.keys(), key=lambda interval: abs(hour - time_to_interval[interval][0]))

def get_data_from_sheets(day, time):

    result = get_sheets()

    if not result:
      return False

    day_index = get_day(day)
    formated_time = get_time_interval(time)
    info(f"Horário: {formated_time} - Dia: {day}")

    for row in result:
      if all(item not in row for item in ['M12','N34','DIAS DA SEMANA']) and row:
          if (row[0] == formated_time and 
            0 < day_index < len(row) and 
            formated_time in allowed_times and 
            row[day_index] != 'X'):

            bolsistas = [bolsista.strip() for bolsista in row[day_index].split('/')]

            if len(bolsistas) == 1:
                info("Bolsista encontrado!")
                return f"Bolsista: {bolsistas[0]}"
            elif len(bolsistas) == 2:
                info("Dois bolsistas encontrados!")
                return f"Bolsistas: {bolsistas[0]} e {bolsistas[1]}"
            elif len(bolsistas) == 3:
                info("Três bolsistas encontrados!")
                return f"Bolsistas: {bolsistas[0]}, {bolsistas[1]} e {bolsistas[2]}"
            
          elif (row[0] == formated_time and 
              row[day_index] == 'X' and 
              formated_time in allowed_times and 
              0 < day_index < len(row)):
            
            info("Horário vazio")
            return "Não tem bolsista neste horário."
          
          elif formated_time not in allowed_times and 0 < day_index < len(row):
            warning("Horário inválido.")
            return False
          
          elif not (0 < day_index < len(row)):
            warning("Dia inválido.")
            return False
          

# if __name__ == "__main__":
#   day = input("Digite o dia: ")
#   time = input("Digite a hora: ")
#   print(get_data_from_sheets(day, time))
    