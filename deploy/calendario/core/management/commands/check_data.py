from django.core.management.base import BaseCommand
from core.models import SolarDate, Event
from datetime import datetime
import pytz

class Command(BaseCommand):
    help = 'Verifica os dados do calendário'

    def handle(self, *args, **options):
        # Define o fuso horário de Brasília
        tz = pytz.timezone('America/Sao_Paulo')
        
        # Verifica datas solares para janeiro de 2025
        start_date = datetime(2025, 1, 1).date()
        end_date = datetime(2025, 1, 31).date()
        
        solar_dates = SolarDate.objects.filter(
            gregorian_date__range=[start_date, end_date]
        )
        
        self.stdout.write(f"Encontradas {solar_dates.count()} datas solares para janeiro/2025")
        
        for solar_date in solar_dates:
            self.stdout.write(f"Data: {solar_date.gregorian_date} - {solar_date.get_display_date()}")
        
        # Verifica eventos
        events = Event.objects.filter(
            gregorian_date__range=[start_date, end_date]
        )
        
        self.stdout.write(f"\nEncontrados {events.count()} eventos para janeiro/2025")
        
        for event in events:
            self.stdout.write(f"Evento: {event.title} em {event.gregorian_date}")
