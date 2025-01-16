from rest_framework import serializers
from .models import Event, BiblicalReference, SolarDate, EventType
from .utils import SolarCalendar
from datetime import datetime

class BiblicalReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BiblicalReference
        fields = ['id', 'book', 'chapter', 'verse', 'text']

class SolarDateSerializer(serializers.ModelSerializer):
    display_date = serializers.CharField(source='get_display_date')

    class Meta:
        model = SolarDate
        fields = ['id', 'gregorian_date', 'solar_day', 'solar_month', 'is_extra_day', 'extra_day_number', 'display_date']

class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = ['id', 'name', 'slug', 'color', 'icon']

class EventSerializer(serializers.ModelSerializer):
    solar_date = SolarDateSerializer(read_only=True)
    biblical_references = BiblicalReferenceSerializer(many=True, read_only=True)
    event_type_new = EventTypeSerializer(read_only=True)
    recurring_event_id = serializers.IntegerField(source='recurring_event.id', read_only=True, allow_null=True)

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'gregorian_date',
            'solar_date', 'event_type', 'event_type_new', 'is_holy_day',
            'sunset_start', 'biblical_references', 'recurring_event_id'
        ]
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Garante que todas as referências bíblicas são incluídas
        if instance.recurring_event and not data.get('biblical_references'):
            data['biblical_references'] = BiblicalReferenceSerializer(
                instance.recurring_event.biblical_references.all(),
                many=True
            ).data
        return data

class CalendarMonthSerializer(serializers.Serializer):
    month = serializers.CharField()
    days = serializers.ListField(child=serializers.DictField())
    events = EventSerializer(many=True)

class DateConverterSerializer(serializers.Serializer):
    gregorian_date = serializers.DateField()
    solar_date = serializers.SerializerMethodField()
    
    def get_solar_date(self, obj):
        date = datetime.combine(obj['gregorian_date'], datetime.min.time())
        return {
            'formatted': SolarCalendar.format_solar_date(date),
            'year': SolarCalendar.get_solar_date(date)[0],
            'month': SolarCalendar.get_solar_date(date)[1],
            'day': SolarCalendar.get_solar_date(date)[2]
        }
