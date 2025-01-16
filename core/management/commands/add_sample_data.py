from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import SolarDate, Event, BiblicalReference
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Adiciona dados de exemplo ao banco de dados'

    def handle(self, *args, **kwargs):
        # Limpa dados existentes
        SolarDate.objects.all().delete()
        Event.objects.all().delete()
        BiblicalReference.objects.all().delete()

        # Cria datas solares para janeiro de 2025
        start_date = datetime(2025, 1, 1).date()
        end_date = datetime(2025, 1, 31).date()
        
        # Meses solares
        solar_months = [
            "Primeiro mês",
            "Segundo mês",
            "Terceiro mês",
            "Quarto mês",
            "Quinto mês",
            "Sexto mês",
            "Sétimo mês",
            "Oitavo mês",
            "Nono mês",
            "Décimo mês",
            "Décimo primeiro mês",
            "Décimo segundo mês",
        ]

        current_date = start_date
        current_solar_day = 1
        current_solar_month = solar_months[0]  # Começando com Primeiro mês

        while current_date <= end_date:
            solar_date = SolarDate.objects.create(
                gregorian_date=current_date,
                solar_day=current_solar_day,
                solar_month=current_solar_month
            )
            
            # Incrementa o dia solar
            current_solar_day += 1
            if current_solar_day > 30:
                current_solar_day = 1
                current_solar_month = solar_months[
                    (solar_months.index(current_solar_month) + 1) % len(solar_months)
                ]
            
            current_date += timedelta(days=1)

        # Cria algumas referências bíblicas
        ref1 = BiblicalReference.objects.create(
            book="Êxodo",
            chapter=12,
            verse="1-2",
            text="E falou o SENHOR a Moisés e a Arão na terra do Egito, dizendo: Este mesmo mês vos será o princípio dos meses; este vos será o primeiro dos meses do ano."
        )

        ref2 = BiblicalReference.objects.create(
            book="Levítico",
            chapter=23,
            verse="4-5",
            text="Estas são as solenidades do SENHOR, as santas convocações, que convocareis ao seu tempo determinado: No mês primeiro, aos catorze do mês, pela tarde, é a páscoa do SENHOR."
        )

        # Cria alguns eventos
        Event.objects.create(
            title="Início do Ano",
            description="Primeiro dia do primeiro mês do ano solar",
            gregorian_date=datetime(2025, 1, 1).date(),
            solar_date=SolarDate.objects.get(gregorian_date=datetime(2025, 1, 1).date()),
            event_type="festival",
            is_holy_day=True,
            sunset_start=True
        ).biblical_references.add(ref1)

        Event.objects.create(
            title="Shabat Semanal",
            description="Dia de descanso e adoração",
            gregorian_date=datetime(2025, 1, 4).date(),
            solar_date=SolarDate.objects.get(gregorian_date=datetime(2025, 1, 4).date()),
            event_type="sabbath",
            is_holy_day=True,
            sunset_start=True
        )

        Event.objects.create(
            title="Rosh Chodesh",
            description="Início do mês lunar",
            gregorian_date=datetime(2025, 1, 15).date(),
            solar_date=SolarDate.objects.get(gregorian_date=datetime(2025, 1, 15).date()),
            event_type="new_month",
            is_holy_day=False,
            sunset_start=True
        )

        self.stdout.write(self.style.SUCCESS('Dados de exemplo adicionados com sucesso!'))
