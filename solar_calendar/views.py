from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services.solar_calculations import get_default_solar_times
from core.models import Event
from datetime import datetime, date

@api_view(['GET'])
def get_solar_info(request):
    """
    Endpoint para obter informações solares
    
    Parâmetros opcionais:
    - date: Data no formato YYYY-MM-DD
    - latitude: Latitude personalizada
    - longitude: Longitude personalizada
    """
    try:
        # Obtém a data
        date_str = request.GET.get('date')
        if date_str:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            date_obj = date.today()

        # Obtém os horários solares
        solar_times = get_default_solar_times(date_obj)
        
        # Obtém eventos sazonais do banco de dados
        year = date_obj.year
        seasonal_events = Event.objects.filter(
            date__year=year,
            event_type__in=['equinox', 'solstice']
        ).order_by('date')

        seasonal_dates = {}
        for event in seasonal_events:
            if 'spring' in event.title.lower():
                seasonal_dates['spring_equinox'] = event.date
            elif 'summer' in event.title.lower():
                seasonal_dates['summer_solstice'] = event.date
            elif 'autumn' in event.title.lower():
                seasonal_dates['autumn_equinox'] = event.date
            elif 'winter' in event.title.lower():
                seasonal_dates['winter_solstice'] = event.date
        
        response_data = {
            'date': date_obj.strftime('%Y-%m-%d'),
            'solar_times': solar_times,
            'seasonal_dates': {
                'spring_equinox': seasonal_dates.get('spring_equinox').strftime('%Y-%m-%d') if seasonal_dates.get('spring_equinox') else None,
                'summer_solstice': seasonal_dates.get('summer_solstice').strftime('%Y-%m-%d') if seasonal_dates.get('summer_solstice') else None,
                'autumn_equinox': seasonal_dates.get('autumn_equinox').strftime('%Y-%m-%d') if seasonal_dates.get('autumn_equinox') else None,
                'winter_solstice': seasonal_dates.get('winter_solstice').strftime('%Y-%m-%d') if seasonal_dates.get('winter_solstice') else None
            }
        }
        
        return Response(response_data)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=400)
