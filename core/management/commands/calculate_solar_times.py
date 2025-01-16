from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import SolarTimes
from astral import LocationInfo
from astral.sun import sun
from datetime import datetime, timedelta, date
from zoneinfo import ZoneInfo
from astral import moon, sun

class Command(BaseCommand):
    help = 'Calcula e armazena os horários solares para um período específico'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=365,
            help='Número de dias para calcular (padrão: 365)'
        )
        parser.add_argument(
            '--latitude',
            type=float,
            default=-15.7801,
            help='Latitude (padrão: Brasília)'
        )
        parser.add_argument(
            '--longitude',
            type=float,
            default=-47.9292,
            help='Longitude (padrão: Brasília)'
        )

    def get_season_type(self, date_obj, location):
        """Determina se a data é um equinócio ou solstício"""
        year = date_obj.year
        
        # Calcula as datas das estações
        spring = sun.spring(year, location.latitude, location.longitude)
        summer = sun.summer(year, location.latitude, location.longitude)
        autumn = sun.autumn(year, location.latitude, location.longitude)
        winter = sun.winter(year, location.latitude, location.longitude)
        
        # Converte para o mesmo fuso horário
        spring = spring.astimezone(date_obj.tzinfo if date_obj.tzinfo else ZoneInfo('America/Sao_Paulo'))
        summer = summer.astimezone(date_obj.tzinfo if date_obj.tzinfo else ZoneInfo('America/Sao_Paulo'))
        autumn = autumn.astimezone(date_obj.tzinfo if date_obj.tzinfo else ZoneInfo('America/Sao_Paulo'))
        winter = winter.astimezone(date_obj.tzinfo if date_obj.tzinfo else ZoneInfo('America/Sao_Paulo'))
        
        # Compara as datas
        if spring.date() == date_obj.date():
            return 'spring_equinox'
        elif summer.date() == date_obj.date():
            return 'summer_solstice'
        elif autumn.date() == date_obj.date():
            return 'autumn_equinox'
        elif winter.date() == date_obj.date():
            return 'winter_solstice'
        
        return None

    def handle(self, *args, **options):
        days = options['days']
        latitude = options['latitude']
        longitude = options['longitude']
        timezone_str = 'America/Sao_Paulo'

        start_date = timezone.now().date()
        location = LocationInfo("Brazil", "South America", timezone_str, latitude, longitude)

        self.stdout.write(f"Calculando horários solares para {days} dias...")
        
        for i in range(days):
            current_date = start_date + timedelta(days=i)
            
            # Verifica se já existe
            solar_times = SolarTimes.objects.filter(date=current_date).first()
            if solar_times:
                continue

            try:
                # Calcula horários solares
                s = sun(location.observer, date=current_date)
                
                # Converte para o fuso horário local
                sunrise = s['sunrise'].astimezone(ZoneInfo(timezone_str))
                sunset = s['sunset'].astimezone(ZoneInfo(timezone_str))
                solar_noon = s['noon'].astimezone(ZoneInfo(timezone_str))

                # Verifica se é um equinócio ou solstício
                season_type = self.get_season_type(sunrise, location)
                is_equinox = season_type and 'equinox' in season_type
                is_solstice = season_type and 'solstice' in season_type

                # Salva no banco de dados
                SolarTimes.objects.create(
                    date=current_date,
                    sunrise=sunrise.time(),
                    sunset=sunset.time(),
                    solar_noon=solar_noon.time(),
                    latitude=latitude,
                    longitude=longitude,
                    is_equinox=is_equinox,
                    is_solstice=is_solstice,
                    season_type=season_type
                )
                
                if i % 10 == 0:  # Mostra progresso a cada 10 dias
                    self.stdout.write(f"Processado até {current_date}")
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Erro ao calcular horários para {current_date}: {str(e)}")
                )

        self.stdout.write(
            self.style.SUCCESS(f"Horários solares calculados com sucesso para {days} dias!")
        )
