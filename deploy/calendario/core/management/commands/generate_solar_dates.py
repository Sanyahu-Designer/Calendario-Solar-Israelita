from django.core.management.base import BaseCommand
from datetime import date, timedelta
from core.models import SolarDate
import calendar

class Command(BaseCommand):
    help = 'Gera datas solares para um período específico'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=365,
            help='Número de dias para gerar (padrão: 365)'
        )

    def handle(self, *args, **options):
        days = options['days']
        start_date = date.today()
        end_date = start_date + timedelta(days=days)
        
        dates_created = 0
        current_date = start_date
        
        while current_date <= end_date:
            # Verifica se a data solar já existe
            if not SolarDate.objects.filter(gregorian_date=current_date).exists():
                # Cria a data solar
                SolarDate.objects.create(
                    gregorian_date=current_date,
                    solar_day=current_date.day,
                    solar_month=calendar.month_name[current_date.month],
                    is_extra_day=False
                )
                dates_created += 1
            
            current_date += timedelta(days=1)
        
        self.stdout.write(
            self.style.SUCCESS(f'Criadas {dates_created} novas datas solares de {start_date} até {end_date}')
        )
