from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from datetime import datetime, date, timedelta
from calendar import monthrange
from astral import LocationInfo
from astral.sun import sun
from zoneinfo import ZoneInfo
from .models import Event, SolarDate
from .serializers import EventSerializer, SolarDateSerializer, BiblicalReferenceSerializer
import pytz
from collections import defaultdict
import traceback
from django.db.models import Min

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_queryset(self):
        try:
            queryset = Event.objects.all().prefetch_related(
                'biblical_references',
                'event_type_new'
            ).select_related('solar_date')
            
            # Filtrar por ano e mês se fornecidos
            year = self.request.query_params.get('year')
            month = self.request.query_params.get('month')
            
            if year and month:
                try:
                    year = int(year)
                    month = int(month)
                    
                    if not (1 <= month <= 12):
                        raise ValueError(f'Mês inválido: {month}. Deve estar entre 1 e 12')
                        
                    _, last_day = monthrange(year, month)
                    start_date = datetime(year, month, 1).date()
                    end_date = datetime(year, month, last_day).date()
                    
                    queryset = queryset.filter(
                        gregorian_date__range=[start_date, end_date]
                    )
                except (ValueError, TypeError) as e:
                    # Log do erro para debug
                    print(f"Erro na validação de parâmetros: {str(e)}")
                    # Retorna queryset vazio em caso de erro
                    return Event.objects.none()
            
            return queryset
        except Exception as e:
            print(f"Erro inesperado em get_queryset: {str(e)}")
            return Event.objects.none()

    def perform_update(self, serializer):
        # Salva o evento
        instance = serializer.save()
        
        # Se este evento foi gerado por um evento recorrente,
        # não propaga as alterações para outros eventos
        if instance.recurring_event:
            return
            
        super().perform_update(serializer)

    @action(detail=True, methods=['get'])
    def references(self, request, pk=None):
        event = self.get_object()
        references = event.biblical_references.all()
        serializer = BiblicalReferenceSerializer(references, many=True)
        return Response(serializer.data)

class CalendarView(APIView):
    def get(self, request):
        try:
            # Validação dos parâmetros
            try:
                year = int(request.query_params.get('year', timezone.now().year))
                month = int(request.query_params.get('month', timezone.now().month))
                
                if not (1 <= month <= 12):
                    return Response(
                        {'error': f'Mês inválido: {month}. Deve estar entre 1 e 12'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except (ValueError, TypeError) as e:
                return Response(
                    {'error': f'Parâmetros inválidos: year={request.query_params.get("year")}, month={request.query_params.get("month")}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            print(f"Received request for year={year}, month={month}")

            # Define o fuso horário de Brasília
            tz = pytz.timezone('America/Sao_Paulo')

            # Obtém o primeiro e último dia do mês
            start_date = datetime(year, month, 1)
            if month == 12:
                end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
            else:
                end_date = datetime(year, month + 1, 1) - timedelta(days=1)

            print(f"Fetching data from {start_date} to {end_date}")

            # Obtém as datas solares do período
            solar_dates = {
                sd.gregorian_date: sd
                for sd in SolarDate.objects.filter(
                    gregorian_date__range=[start_date.date(), end_date.date()]
                ).order_by('gregorian_date')
            }
            print(f"Found {len(solar_dates)} solar dates")

            # Obtém todos os eventos do período
            events = Event.objects.filter(
                gregorian_date__range=[start_date.date(), end_date.date()]
            ).select_related(
                'solar_date',
                'event_type_new',
                'recurring_event'
            ).prefetch_related(
                'biblical_references'
            ).order_by('gregorian_date', 'title')
            
            print(f"Found {events.count()} events")
            
            # Remove duplicatas manualmente
            events_by_key = {}
            for event in events:
                key = (event.gregorian_date, event.title)
                if key not in events_by_key or event.id < events_by_key[key].id:
                    events_by_key[key] = event
            
            # Converte de volta para lista
            events = sorted(events_by_key.values(), key=lambda e: (e.gregorian_date, e.title))
            
            print(f"After removing duplicates: {len(events)} events")
            
            events_by_date = defaultdict(list)
            for event in events:
                events_by_date[event.gregorian_date].append(event)
            print(f"Grouped events for {len(events_by_date)} dates")

            # Gera os dias do calendário apenas para o mês atual
            days = []
            current_date = start_date
            while current_date <= end_date:
                solar_date = solar_dates.get(current_date.date())
                events = events_by_date[current_date.date()]
                
                try:
                    day_data = {
                        'gregorian_date': current_date.date().isoformat(),
                        'solar_date': SolarDateSerializer(solar_date).data if solar_date else None,
                        'events': EventSerializer(events, many=True).data
                    }
                    days.append(day_data)
                except Exception as e:
                    print(f"Error processing date {current_date}: {str(e)}")
                    raise
                
                current_date += timedelta(days=1)

            # Ordena os dias pelo dia gregoriano
            days.sort(key=lambda x: datetime.strptime(x['gregorian_date'], '%Y-%m-%d'))

            response_data = {
                'year': year,
                'month': month,
                'days': days
            }
            print(f"Returning calendar with {len(days)} days")
            return Response(response_data)
        except Exception as e:
            import traceback
            print(f"Error in calendar view: {str(e)}")
            print(traceback.format_exc())
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class SolarTimesView(APIView):
    def get(self, request):
        try:
            # Obtém os parâmetros da requisição
            date_str = request.query_params.get('date')
            latitude = float(request.query_params.get('latitude', -15.7801))  # Padrão: Brasília
            longitude = float(request.query_params.get('longitude', -47.9292))  # Padrão: Brasília
            
            if not date_str:
                target_date = timezone.now().date()
                year = target_date.year
                month = target_date.month
            else:
                try:
                    # Tenta primeiro como data completa YYYY-MM-DD
                    if len(date_str.split('-')) == 3:
                        year, month, day = map(int, date_str.split('-'))
                        target_date = date(year, month, day)
                    else:
                        # Se falhar, tenta como YYYY-MM
                        year, month = map(int, date_str.split('-'))
                        target_date = date(year, month, 1)
                except (ValueError, TypeError) as e:
                    return Response(
                        {'error': f'Formato de data inválido: {date_str}. Use YYYY-MM-DD ou YYYY-MM'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Calcula o primeiro e último dia do mês
            _, last_day = monthrange(year, month)
            start_date = date(year, month, 1)
            end_date = date(year, month, last_day)

            # Configura a localização
            timezone_str = 'America/Sao_Paulo'
            location = LocationInfo(
                "Custom Location",
                "Region",
                timezone_str,
                latitude,
                longitude
            )

            # Datas dos equinócios e solstícios para 2025
            equinoxes_solstices = {
                '2025-03-20': {'type': 'spring_equinox', 'time': '12:01'},
                '2025-06-21': {'type': 'summer_solstice', 'time': '02:42'},
                '2025-09-22': {'type': 'autumn_equinox', 'time': '14:19'},
                '2025-12-21': {'type': 'winter_solstice', 'time': '22:03'}
            }

            # Calcula os horários solares para cada dia do mês
            data = []
            current_date = start_date
            while current_date <= end_date:
                try:
                    # Calcula horários solares usando Astral
                    s = sun(location.observer, date=current_date)
                    
                    # Converte para o fuso horário local
                    sunrise = s['sunrise'].astimezone(ZoneInfo(timezone_str))
                    sunset = s['sunset'].astimezone(ZoneInfo(timezone_str))
                    solar_noon = s['noon'].astimezone(ZoneInfo(timezone_str))

                    # Verifica se é um dia de equinócio ou solstício
                    current_date_str = current_date.isoformat()
                    season_info = equinoxes_solstices.get(current_date_str)
                    
                    # Adiciona ao resultado
                    data.append({
                        'date': current_date_str,
                        'sunrise': sunrise.strftime('%H:%M'),
                        'sunset': sunset.strftime('%H:%M'),
                        'solar_noon': solar_noon.strftime('%H:%M'),
                        'latitude': latitude,
                        'longitude': longitude,
                        'season_type': season_info['type'] if season_info else None,
                        'season_time': season_info['time'] if season_info else None
                    })
                except Exception as e:
                    print(f"Erro ao calcular horários solares para {current_date}: {str(e)}")
                
                current_date += timedelta(days=1)

            if data:
                return Response(data)
            else:
                return Response(
                    {'error': 'Não foi possível calcular os horários solares'},
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class DateConverterView(APIView):
    def post(self, request):
        try:
            gregorian_date = request.data.get('gregorian_date')
            if not gregorian_date:
                return Response(
                    {'error': 'gregorian_date é obrigatório'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            date_obj = datetime.strptime(gregorian_date, '%Y-%m-%d').date()
            
            try:
                solar_date = SolarDate.objects.get(gregorian_date=date_obj)
                return Response(SolarDateSerializer(solar_date).data)
            except SolarDate.DoesNotExist:
                return Response(
                    {'error': 'Data solar não encontrada'},
                    status=status.HTTP_404_NOT_FOUND
                )
        except ValueError:
            return Response(
                {'error': 'Formato de data inválido. Use YYYY-MM-DD'},
                status=status.HTTP_400_BAD_REQUEST
            )
