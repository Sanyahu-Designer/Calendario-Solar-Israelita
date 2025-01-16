from django.core.management.base import BaseCommand
from core.models import Event, RecurringEvent, SolarDate
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Debug do evento recorrente do Shabbat'

    def handle(self, *args, **options):
        # Encontra o evento recorrente do Shabbat
        shabbat = RecurringEvent.objects.filter(
            title__icontains='Shabbat',
            recurrence_type='weekly'
        ).first()

        if not shabbat:
            self.stdout.write(self.style.ERROR('Evento recorrente do Shabbat não encontrado'))
            return

        self.stdout.write(f'\nEvento Recorrente encontrado:')
        self.stdout.write(f'Título: {shabbat.title}')
        self.stdout.write(f'Tipo: {shabbat.recurrence_type}')
        self.stdout.write(f'Dia da semana: {shabbat.weekday}')
        self.stdout.write(f'Data de início: {shabbat.start_date}')
        self.stdout.write(f'Data de fim: {shabbat.end_date}')
        self.stdout.write(f'Última geração: {shabbat.last_generated_date}')

        # Verifica eventos existentes
        events = Event.objects.filter(recurring_event=shabbat).order_by('gregorian_date')
        self.stdout.write(f'\nEventos gerados ({events.count()}):')
        for event in events:
            self.stdout.write(f'- {event.gregorian_date}: {event.title}')

        # Verifica datas solares
        start_date = date(2025, 1, 1)
        end_date = date(2025, 3, 31)
        current = start_date
        missing_dates = []

        self.stdout.write(f'\nVerificando datas solares de {start_date} até {end_date}:')
        while current <= end_date:
            if current.weekday() == shabbat.weekday:  # Verifica apenas sábados
                solar_date = SolarDate.objects.filter(gregorian_date=current).first()
                if not solar_date:
                    missing_dates.append(current)
            current += timedelta(days=1)

        if missing_dates:
            self.stdout.write(self.style.WARNING(f'\nDatas solares faltando para sábados:'))
            for d in missing_dates:
                self.stdout.write(f'- {d}')
        else:
            self.stdout.write(self.style.SUCCESS('\nTodas as datas solares necessárias estão presentes'))
