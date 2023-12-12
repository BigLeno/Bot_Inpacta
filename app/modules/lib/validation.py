from time import strptime

def is_valid_date(date_str) -> bool:
    """Verifica se a data está no formato dd/mm."""

    if date_str in ['hoje', 'amanhã', 'amanha']:
        return True

    try:
        strptime(date_str, '%d/%m')
        return True
    except ValueError:
        return False

def is_valid_time(time_str) -> bool:
    """Verifica se o horário está no formato hh:mm."""
    formats = ['%H:%M', '%Hh', '%Hh%M', '%HH', '%HH%M']
    for fmt in formats:
        try:
            strptime(time_str, fmt)
            return True
        except ValueError:
            continue
    return False