from datetime import datetime, timedelta
from typing import Tuple, Dict

class SolarCalendar:
    MONTHS = [
        'Abibe', 'Zife', 'Sivã', 'Tamuz', 
        'Ave', 'Elul', 'Etanim', 'Bul',
        'Quisleu', 'Tebete', 'Sebate', 'Adare'
    ]
    
    # Datas aproximadas dos equinócios
    EQUINOX_DATES = {
        2024: datetime(2024, 3, 19),  # Equinócio de Primavera 2024
        2025: datetime(2025, 3, 20),  # Equinócio de Primavera 2025
    }
    
    @classmethod
    def get_spring_equinox(cls, year: int) -> datetime:
        """Retorna a data do equinócio de primavera para um determinado ano."""
        if year in cls.EQUINOX_DATES:
            return cls.EQUINOX_DATES[year]
        # Se o ano não estiver mapeado, usa o mais próximo
        return datetime(year, 3, 20)  # Data média do equinócio
    
    @classmethod
    def get_solar_year(cls, date: datetime) -> int:
        """Calcula o ano solar baseado na data gregoriana."""
        if date.month < 3 or (date.month == 3 and date.day < 20):
            return date.year - 1
        return date.year
    
    @classmethod
    def get_solar_date(cls, gregorian_date: datetime) -> Tuple[int, str, int]:
        """
        Converte uma data gregoriana para o calendário solar.
        Retorna: (ano, mês, dia)
        """
        solar_year = cls.get_solar_year(gregorian_date)
        
        # Obtém o equinócio para o ano em questão
        spring_equinox = cls.get_spring_equinox(solar_year)
        
        # Se a data é antes do equinócio de primavera, usa o ano anterior
        if gregorian_date < spring_equinox:
            solar_year -= 1
            spring_equinox = cls.get_spring_equinox(solar_year)
        
        # Calcula o número de dias desde o início do ano solar
        days_since_new_year = (gregorian_date - spring_equinox).days
        
        # Calcula o mês e o dia
        month_index = days_since_new_year // 30
        day = (days_since_new_year % 30) + 1
        
        # Ajusta para não ultrapassar o último mês
        if month_index >= len(cls.MONTHS):
            month_index = len(cls.MONTHS) - 1
            day = 30
        
        return solar_year, cls.MONTHS[month_index], day
    
    @classmethod
    def format_solar_date(cls, gregorian_date: datetime) -> str:
        """Formata a data solar como string."""
        year, month, day = cls.get_solar_date(gregorian_date)
        return f"{day} de {month}, {year}"
    
    @classmethod
    def get_festival_dates(cls, year: int) -> Dict[str, datetime]:
        """
        Retorna as datas dos principais festivais para um determinado ano.
        """
        spring_equinox = cls.get_spring_equinox(year)
        
        return {
            'Pessach': spring_equinox + timedelta(days=14),  # 14 dias após o equinócio
            'Pães Ázimos': spring_equinox + timedelta(days=15),  # 15 dias após o equinócio
            'Primícias': spring_equinox + timedelta(days=16),  # 16 dias após o equinócio
            'Pentecostes': spring_equinox + timedelta(days=65),  # 50 dias após as Primícias
            'Trombetas': spring_equinox + timedelta(days=186),  # 1º dia do 7º mês
            'Expiação': spring_equinox + timedelta(days=195),  # 10º dia do 7º mês
            'Tabernáculos': spring_equinox + timedelta(days=200),  # 15º dia do 7º mês
        }
