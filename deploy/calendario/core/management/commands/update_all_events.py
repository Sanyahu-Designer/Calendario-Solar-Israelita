from django.core.management.base import BaseCommand
from core.models import Event, RecurringEvent
from django.db import transaction

class Command(BaseCommand):
    help = 'Atualiza todos os eventos existentes com as informações mais recentes dos eventos recorrentes'

    def handle(self, *args, **options):
        with transaction.atomic():
            # Atualiza todos os eventos de Shabat/Shabbat
            events = Event.objects.filter(title__icontains='Shabat')
            
            if events.exists():
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Encontrados {events.count()} eventos para atualizar'
                    )
                )
                
                # Atualiza os eventos
                for event in events:
                    event.title = "Shabbat semanal"
                    event.event_type = 'sabbath'
                    event.is_holy_day = True
                    event.save()
                    
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Atualizados {events.count()} eventos para Shabbat'
                    )
                )
