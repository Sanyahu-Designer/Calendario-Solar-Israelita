from django.core.management.base import BaseCommand
from core.models import Event, RecurringEvent
from django.db import transaction
from django.db.models import Q

class Command(BaseCommand):
    help = 'Corrige os eventos de Shabbat'

    def handle(self, *args, **options):
        with transaction.atomic():
            # Encontra todos os eventos de Shabat/Shabbat
            events = Event.objects.filter(
                Q(title__icontains='Shabat') | Q(title__icontains='Shabbat')
            )
            
            if events.exists():
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Encontrados {events.count()} eventos para corrigir'
                    )
                )
                
                # Atualiza os eventos
                count = events.update(
                    title="Shabbat semanal",
                    event_type='sabbath',
                    is_holy_day=True
                )
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Atualizados {count} eventos para Shabbat'
                    )
                )
                
            # Atualiza o evento recorrente
            recurring_event = RecurringEvent.objects.filter(
                Q(title__icontains='Shabat') | Q(title__icontains='Shabbat')
            ).first()
            
            if recurring_event:
                recurring_event.title = "Shabbat semanal"
                recurring_event.event_type = 'sabbath'
                recurring_event.is_holy_day = True
                recurring_event.save()
                
                self.stdout.write(
                    self.style.SUCCESS(
                        'Evento recorrente atualizado para Shabbat'
                    )
                )
