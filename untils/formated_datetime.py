from datetime import datetime
import pytz

def date_now(db_log: bool = False):
    """retorna data e hora formatada para cada ambiente"""
    
    brt_timezone = pytz.timezone('America/Sao_Paulo')
    
    if db_log:
        data_hora = datetime.now(brt_timezone)
        return data_hora.strftime("%Y-%m-%dT%H:%M:%S")
    else:
        data_hora = datetime.now(brt_timezone)
        return data_hora.strftime("%d/%m/%Y %H:%M:%S")
    
def format_date(date):
    """formata data e hora para o usuario"""
    if date != "":
        dt_origin = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
        return dt_origin.strftime("%d/%m/%Y %H:%M:%S")
