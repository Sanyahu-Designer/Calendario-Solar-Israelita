import os
import django

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biodinamico.settings')
django.setup()

from core.models import Event, EventType

# Obter todos os tipos de eventos
event_types = {et.slug: et for et in EventType.objects.all()}

# Atualizar todos os eventos
for event in Event.objects.all():
    event_type_slug = event.event_type
    if event_type_slug in event_types:
        event.event_type_new = event_types[event_type_slug]
        event.save()
        print(f'Atualizado evento "{event.title}" com tipo "{event_types[event_type_slug].name}"')
