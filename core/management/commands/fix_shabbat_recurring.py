from django.core.management.base import BaseCommand
from core.models import RecurringEvent
from datetime import date

class Command(BaseCommand):
    help = 'Remove a data de fim do evento recorrente do Shabbat e gera eventos'

    def handle(self, *args, **options):
        # Encontra o evento recorrente do Shabbat
        shabbat = RecurringEvent.objects.filter(
            title__icontains='Shabbat',
            recurrence_type='weekly'
        ).first()

        if not shabbat:
            self.stdout.write(self.style.ERROR('Evento recorrente do Shabbat não encontrado'))
            return

        # Remove a data de fim
        self.stdout.write(f'Data de fim atual: {shabbat.end_date}')
        shabbat.end_date = None
        shabbat.save()
        self.stdout.write(self.style.SUCCESS('Data de fim removida'))

        # Tenta gerar eventos até o final de 2025
        until_date = date(2025, 12, 31)
        self.stdout.write(f'Gerando eventos até {until_date}')
        
        events_created = shabbat.generate_events(until_date)
        
        self.stdout.write(self.style.SUCCESS(f'Processo finalizado. {events_created} eventos criados.'))
