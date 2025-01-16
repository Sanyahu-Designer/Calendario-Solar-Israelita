from django.core.management.base import BaseCommand
from core.models import EventType

class Command(BaseCommand):
    help = 'Cria os tipos de eventos padrão'

    def handle(self, *args, **options):
        event_types = [
            {
                'name': 'Festival Bíblico',
                'slug': 'biblical_festival',
                'description': 'Festas e celebrações bíblicas',
                'color': '#FF0000',
                'icon': '🎉'
            },
            {
                'name': 'Evento Histórico',
                'slug': 'historical',
                'description': 'Eventos históricos importantes',
                'color': '#0000FF',
                'icon': '📚'
            },
            {
                'name': 'Shabat',
                'slug': 'sabbath',
                'description': 'Dia de descanso semanal',
                'color': '#800080',
                'icon': '✡️'
            },
            {
                'name': 'Rosh Chodesh',
                'slug': 'new_month',
                'description': 'Início do mês lunar',
                'color': '#008000',
                'icon': '🌙'
            },
            {
                'name': 'Equinócio',
                'slug': 'equinox',
                'description': 'Equinócio solar',
                'color': '#FFA500',
                'icon': '☀️'
            },
            {
                'name': 'Solstício',
                'slug': 'solstice',
                'description': 'Solstício solar',
                'color': '#FFD700',
                'icon': '🌞'
            },
            {
                'name': 'Tekufah',
                'slug': 'tekufah',
                'description': 'Mudança de estação',
                'color': '#4B0082',
                'icon': '🌱'
            }
        ]

        for event_type in event_types:
            EventType.objects.get_or_create(
                slug=event_type['slug'],
                defaults=event_type
            )
            self.stdout.write(f'Criado tipo de evento "{event_type["name"]}"')
