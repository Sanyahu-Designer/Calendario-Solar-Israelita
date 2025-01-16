from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import RecurringEvent, Event, SolarDate
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Corrige configurações do Shabbat e gera eventos'

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                # Encontra o evento recorrente do Shabbat
                shabbat = RecurringEvent.objects.filter(
                    title__icontains='Shabbat',
                    recurrence_type='weekly'
                ).first()

                if not shabbat:
                    self.stdout.write(self.style.ERROR('Evento recorrente do Shabbat não encontrado'))
                    return

                # Backup das configurações antigas
                self.stdout.write('Configurações antigas:')
                self.stdout.write(f'- Data início: {shabbat.start_date}')
                self.stdout.write(f'- Data fim: {shabbat.end_date}')
                self.stdout.write(f'- Dia santo: {shabbat.is_holy_day}')
                self.stdout.write(f'- Começa no pôr do sol: {shabbat.sunset_start}')

                # Atualiza apenas as configurações necessárias
                shabbat.is_holy_day = True
                shabbat.sunset_start = True
                shabbat.save()

                self.stdout.write(self.style.SUCCESS('\nConfigurações atualizadas com sucesso'))

                # Remove eventos antigos
                deleted_count = Event.objects.filter(recurring_event=shabbat).delete()[0]
                self.stdout.write(f'\n{deleted_count} eventos antigos removidos')

                # Verifica datas solares disponíveis
                start_date = shabbat.start_date
                end_date = shabbat.end_date or date(2025, 12, 31)
                
                self.stdout.write('\nVerificando datas solares...')
                available_dates = []
                skipped_dates = []
                current = start_date
                
                while current <= end_date:
                    if current.weekday() == 5:  # Sábado
                        if SolarDate.objects.filter(gregorian_date=current).exists():
                            available_dates.append(current)
                        else:
                            skipped_dates.append(current)
                    current += timedelta(days=7)

                self.stdout.write(f'\nDatas solares disponíveis: {len(available_dates)}')
                self.stdout.write(f'Datas solares faltando: {len(skipped_dates)}')

                if skipped_dates:
                    self.stdout.write('\nAs seguintes datas serão puladas (sem data solar):')
                    for d in skipped_dates:
                        self.stdout.write(f'- {d}')

                if available_dates:
                    self.stdout.write('\nGerando eventos para as datas disponíveis...')
                    events_created = 0
                    for event_date in available_dates:
                        if shabbat._create_event(event_date):
                            events_created += 1
                    
                    # Verifica se os eventos foram realmente criados
                    actual_events = Event.objects.filter(recurring_event=shabbat).count()
                    
                    if actual_events > 0 and actual_events == events_created:
                        self.stdout.write(self.style.SUCCESS(
                            f'\nSucesso! {events_created} eventos criados e verificados no banco'
                        ))
                    else:
                        self.stdout.write(self.style.ERROR(
                            f'\nErro: {events_created} eventos deveriam ter sido criados, '
                            f'mas apenas {actual_events} foram encontrados no banco'
                        ))
                else:
                    self.stdout.write(self.style.WARNING('\nNenhuma data solar disponível no período'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\nErro: {str(e)}'))
