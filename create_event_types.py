import os
import django

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calendario_solar.settings')
django.setup()

from core.models import EventType

# Lista de tipos de eventos padrão
default_event_types = [
    {
        'name': 'Festival Bíblico',
        'slug': 'festival',
        'description': 'Festivais e Celebrações Bíblicas',
        'color': '#FF0000',
        'icon': '🎉',
        'order': 1,
    },
    {
        'name': 'Evento Histórico',
        'slug': 'historical',
        'description': 'Eventos Históricos Importantes',
        'color': '#0000FF',
        'icon': '📚',
        'order': 2,
    },
    {
        'name': 'Shabat',
        'slug': 'sabbath',
        'description': 'Dia de Descanso Semanal',
        'color': '#800080',
        'icon': '✡️',
        'order': 3,
    },
    {
        'name': 'Rosh Chodesh',
        'slug': 'new_month',
        'description': 'Início do Mês Solar',
        'color': '#008000',
        'icon': '🌒',
        'order': 4,
    },
    {
        'name': 'Equinócio',
        'slug': 'equinox',
        'description': 'Equinócios de Primavera e Outono',
        'color': '#FFA500',
        'icon': '⚖️',
        'order': 5,
    },
    {
        'name': 'Solstício',
        'slug': 'solstice',
        'description': 'Solstícios de Verão e Inverno',
        'color': '#FFD700',
        'icon': '☀️',
        'order': 6,
    },
    {
        'name': 'Tekufah',
        'slug': 'tekufah',
        'description': 'Mudança de Estação',
        'color': '#98FB98',
        'icon': '🌱',
        'order': 7,
    },
]

def create_event_types():
    print("Criando tipos de eventos...")
    for event_type in default_event_types:
        EventType.objects.get_or_create(
            slug=event_type['slug'],
            defaults=event_type
        )
    print("Tipos de eventos criados com sucesso!")

if __name__ == '__main__':
    create_event_types()
