from django.core.management.base import BaseCommand
from core.models import Event, RecurringEvent
from django.db import transaction

class Command(BaseCommand):
    help = 'Associa eventos existentes aos seus eventos recorrentes'

    def handle(self, *args, **options):
        with transaction.atomic():
            # Para cada evento recorrente
            for recurring_event in RecurringEvent.objects.all():
                # Encontra todos os eventos com o mesmo título
                events = Event.objects.filter(
                    title=recurring_event.title,
                    recurring_event__isnull=True
                )
                
                # Atualiza os eventos encontrados
                count = events.update(
                    recurring_event=recurring_event,
                    event_type=recurring_event.event_type,
                    event_type_new=recurring_event.event_type_new,
                    is_holy_day=recurring_event.is_holy_day,
                    sunset_start=recurring_event.sunset_start
                )
                
                if count > 0:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Associados {count} eventos ao evento recorrente "{recurring_event.title}"'
                        )
                    )
                    
                    # Atualiza as referências bíblicas
                    for event in events:
                        event.biblical_references.set(recurring_event.biblical_references.all())
