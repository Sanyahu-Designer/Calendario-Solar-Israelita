from astral import LocationInfo
from astral.sun import sun
from datetime import datetime, timedelta, date
from zoneinfo import ZoneInfo
from core.models import SolarTimes

def get_solar_times(date_obj, latitude=-15.7801, longitude=-47.9292, timezone='America/Sao_Paulo'):
    """
    Calcula horários solares para uma data e localização específicas.
    
    Args:
        date_obj (date): Data para cálculo
        latitude (float): Latitude da localização
        longitude (float): Longitude da localização
        timezone (str): Fuso horário
    
    Returns:
        dict: Horários solares formatados
    """
    try:
        # Verifica se já existe no banco de dados
        cached_times = SolarTimes.objects.filter(
            date=date_obj,
            latitude=latitude,
            longitude=longitude
        ).first()

        if cached_times:
            return {
                'sunrise': cached_times.sunrise.strftime('%H:%M'),
                'sunset': cached_times.sunset.strftime('%H:%M'),
                'solar_noon': cached_times.solar_noon.strftime('%H:%M')
            }

        # Localização
        location = LocationInfo("Brazil", "South America", timezone, latitude, longitude)
        
        # Calcula horários solares
        s = sun(location.observer, date=date_obj)
        
        # Converte para o fuso horário local
        sunrise = s['sunrise'].astimezone(ZoneInfo(timezone))
        sunset = s['sunset'].astimezone(ZoneInfo(timezone))
        solar_noon = s['noon'].astimezone(ZoneInfo(timezone))

        # Salva no banco de dados
        SolarTimes.objects.create(
            date=date_obj,
            sunrise=sunrise.time(),
            sunset=sunset.time(),
            solar_noon=solar_noon.time(),
            latitude=latitude,
            longitude=longitude
        )

        return {
            'sunrise': sunrise.strftime('%H:%M'),
            'sunset': sunset.strftime('%H:%M'),
            'solar_noon': solar_noon.strftime('%H:%M')
        }
    except Exception as e:
        print(f"Erro no cálculo solar: {e}")
        return None

def get_default_solar_times(date_obj=None):
    """
    Retorna horários solares para localização padrão (Brasília)
    
    Args:
        date_obj (date, optional): Data para cálculo. Padrão é hoje.
    
    Returns:
        dict: Horários solares
    """
    if date_obj is None:
        date_obj = date.today()
    elif isinstance(date_obj, datetime):
        date_obj = date_obj.date()
    
    return get_solar_times(date_obj)
