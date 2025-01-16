from django.db import models
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.

class SolarDate(models.Model):
    gregorian_date = models.DateField()
    solar_day = models.IntegerField(null=True, blank=True)  # Opcional para dias extras
    solar_month = models.CharField(max_length=50, null=True, blank=True)  # Opcional para dias extras
    is_extra_day = models.BooleanField(default=False)  # Indica se é um dia de acréscimo
    extra_day_number = models.IntegerField(null=True, blank=True)  # Número do dia de acréscimo (1 a 5)

    class Meta:
        ordering = ['gregorian_date']

    def __str__(self):
        if self.is_extra_day:
            return f"Dia +{self.extra_day_number} (gregoriano: {self.gregorian_date})"
        return f"Dia {self.solar_day} do {self.solar_month} (gregoriano: {self.gregorian_date})"

    def get_display_date(self):
        """Retorna a representação da data para exibição"""
        if self.is_extra_day:
            return f"+{self.extra_day_number}"
        return f"{self.solar_day} do {self.solar_month}"


class EventType(models.Model):
    name = models.CharField('Nome', max_length=50, unique=True)
    slug = models.SlugField('Identificador', max_length=50, unique=True)
    description = models.TextField('Descrição', blank=True)
    color = models.CharField('Cor', max_length=20, help_text='Cor para exibição no calendário (ex: #FF0000)', blank=True)
    icon = models.CharField('Ícone', max_length=20, help_text='Emoji ou código do ícone', blank=True)
    order = models.IntegerField('Ordem', default=0, help_text='Ordem de exibição no calendário')

    class Meta:
        verbose_name = 'Tipo de Evento'
        verbose_name_plural = 'Tipos de Eventos'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class SolarTimes(models.Model):
    date = models.DateField(unique=True)
    sunrise = models.TimeField()
    sunset = models.TimeField()
    solar_noon = models.TimeField()
    latitude = models.FloatField(default=-15.7801)  # Brasília por padrão
    longitude = models.FloatField(default=-47.9292)  # Brasília por padrão
    is_equinox = models.BooleanField(default=False)
    is_solstice = models.BooleanField(default=False)
    season_type = models.CharField(max_length=20, blank=True, null=True,
                                 choices=[
                                     ('spring_equinox', 'Equinócio de Primavera'),
                                     ('summer_solstice', 'Solstício de Verão'),
                                     ('autumn_equinox', 'Equinócio de Outono'),
                                     ('winter_solstice', 'Solstício de Inverno'),
                                 ])

    class Meta:
        verbose_name = 'Horário Solar'
        verbose_name_plural = 'Horários Solares'
        ordering = ['date']

    def __str__(self):
        return f"Horários solares para {self.date}"


class Event(models.Model):
    EVENT_TYPES = [
        ('festival', 'Festival Bíblico'),
        ('historical', 'Evento Histórico'),
        ('sabbath', 'Shabbat'),
        ('new_month', 'Rosh Chodesh'),
        ('equinox', 'Equinócio'),
        ('solstice', 'Solstício'),
        ('tekufah', 'Tekufah'),
    ]

    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descrição', blank=True)
    gregorian_date = models.DateField('Data Gregoriana', default=timezone.now)
    solar_date = models.ForeignKey(SolarDate, verbose_name='Data Solar', on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField('Tipo de Evento', max_length=20, choices=EVENT_TYPES, default='historical')
    event_type_new = models.ForeignKey(EventType, verbose_name='Novo Tipo de Evento', 
                                     on_delete=models.SET_NULL, null=True, blank=True, 
                                     related_name='events')
    is_holy_day = models.BooleanField('Dia de Shabbat', default=False)
    sunset_start = models.BooleanField('Começa no Pôr do Sol', default=True)
    biblical_references = models.ManyToManyField('BiblicalReference', verbose_name='Referências Bíblicas', blank=True)
    recurring_event = models.ForeignKey('RecurringEvent', verbose_name='Evento Recorrente',
                                      on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='generated_events')
    
    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['gregorian_date', 'title']

    def __str__(self):
        return f"{self.title} ({self.gregorian_date})"


class BiblicalReference(models.Model):
    book = models.CharField(max_length=50)
    chapter = models.IntegerField()
    verse = models.CharField(max_length=10)
    text = models.TextField()

    class Meta:
        verbose_name = 'Referência Bíblica'
        verbose_name_plural = 'Referências Bíblicas'
        ordering = ['book', 'chapter']

    def __str__(self):
        return f"{self.book} {self.chapter}:{self.verse}"


class RecurringEvent(models.Model):
    RECURRENCE_TYPES = [
        ('weekly', 'Semanal'),
        ('annual', 'Anual'),
        ('lunar', 'Lunar'),
    ]

    WEEKDAYS = [
        (4, 'Sexta-feira'),  # Para eventos que começam no pôr do sol
        (5, 'Sábado'),
    ]

    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descrição', blank=True)
    recurrence_type = models.CharField('Tipo de Recorrência', max_length=10, choices=RECURRENCE_TYPES)
    
    # Para eventos semanais (ex: Shabat)
    weekday = models.IntegerField('Dia da Semana', choices=WEEKDAYS, null=True, blank=True)
    
    # Para eventos anuais (ex: Pessach)
    annual_month = models.IntegerField('Mês', null=True, blank=True)
    annual_day = models.IntegerField('Dia', null=True, blank=True)
    
    # Configurações gerais
    event_type = models.CharField('Tipo de Evento', max_length=20, choices=Event.EVENT_TYPES, default='historical')
    event_type_new = models.ForeignKey(EventType, verbose_name='Novo Tipo de Evento', 
                                     on_delete=models.SET_NULL, null=True, blank=True)
    is_holy_day = models.BooleanField('Dia de Shabbat', default=False)
    sunset_start = models.BooleanField('Começa no Pôr do Sol', default=True)
    
    # Período de validade
    start_date = models.DateField('Data de Início')
    end_date = models.DateField('Data de Fim', null=True, blank=True)
    
    # Referências bíblicas
    biblical_references = models.ManyToManyField('BiblicalReference', verbose_name='Referências Bíblicas', blank=True)
    
    # Controle de geração
    last_generated_date = models.DateField('Última Geração', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Evento Recorrente'
        verbose_name_plural = 'Eventos Recorrentes'
        ordering = ['title']

    def __str__(self):
        return f"{self.title} ({self.get_recurrence_type_display()})"

    def generate_events(self, until_date=None):
        """
        Gera eventos baseados na recorrência até a data especificada
        """
        from datetime import datetime, timedelta, date
        import calendar
        from django.utils import timezone
        from django.db import transaction
        
        if not until_date:
            # Gera eventos para o próximo ano
            until_date = date.today() + timedelta(days=365)
        
        if self.end_date and self.end_date < until_date:
            until_date = self.end_date
            
        current_date = max(self.start_date, date.today())
        events_created = 0
        
        try:
            with transaction.atomic():
                # Remove eventos existentes que ainda não aconteceram
                Event.objects.filter(
                    recurring_event=self,
                    gregorian_date__gte=date.today()
                ).delete()
                
                # Mantém registro de datas já processadas para evitar duplicatas
                processed_dates = set()
                
                if self.recurrence_type == 'weekly' and self.weekday is not None:
                    # Para eventos semanais (ex: Shabat)
                    while current_date <= until_date:
                        # Encontra o próximo dia da semana desejado
                        while current_date.weekday() != self.weekday:
                            current_date += timedelta(days=1)
                        
                        if current_date <= until_date and current_date not in processed_dates:
                            # Verifica se existe data solar antes de tentar criar
                            if SolarDate.objects.filter(gregorian_date=current_date).exists():
                                if self._create_event(current_date):
                                    events_created += 1
                                    processed_dates.add(current_date)
                        
                        # Avança para a próxima semana
                        current_date += timedelta(days=7)
                        
                elif self.recurrence_type == 'annual' and self.annual_month and self.annual_day:
                    # Para eventos anuais
                    while current_date.year <= until_date.year:
                        try:
                            event_date = date(current_date.year, self.annual_month, self.annual_day)
                            if self.start_date <= event_date <= until_date and event_date not in processed_dates:
                                # Verifica se existe data solar antes de tentar criar
                                if SolarDate.objects.filter(gregorian_date=event_date).exists():
                                    if self._create_event(event_date):
                                        events_created += 1
                                        processed_dates.add(event_date)
                        except ValueError:
                            pass  # Ignora datas inválidas
                        
                        current_date = date(current_date.year + 1, 1, 1)
                
        except Exception as e:
            print(f"Erro ao gerar eventos: {str(e)}")
            raise e
        
        return events_created

    def _create_event(self, event_date):
        """
        Cria um evento individual baseado no evento recorrente
        Retorna True se o evento foi criado, False caso contrário
        """
        from django.db import transaction
        
        try:
            with transaction.atomic():
                # Encontra a data solar correspondente
                solar_date = SolarDate.objects.filter(gregorian_date=event_date).first()
                
                if not solar_date:
                    return False
                
                # Define o valor padrão de sunset_start baseado no tipo de evento
                sunset_start = True
                if self.event_type == 'sabbath':
                    sunset_start = False
                
                # Verifica se já existe um evento para esta data e título
                existing_event = Event.objects.filter(
                    gregorian_date=event_date,
                    title=self.title
                ).first()
                
                if existing_event:
                    # Se o evento existente é deste mesmo evento recorrente, atualiza-o
                    if existing_event.recurring_event_id == self.id:
                        existing_event.description = self.description
                        existing_event.event_type = self.event_type
                        existing_event.event_type_new = self.event_type_new
                        existing_event.is_holy_day = self.is_holy_day
                        existing_event.sunset_start = sunset_start
                        existing_event.save()
                        
                        # Atualiza referências bíblicas
                        existing_event.biblical_references.set(self.biblical_references.all())
                        return True
                    return False
                
                # Cria o evento
                event = Event.objects.create(
                    title=self.title,
                    description=self.description,
                    gregorian_date=event_date,
                    solar_date=solar_date,
                    event_type=self.event_type,
                    event_type_new=self.event_type_new,
                    is_holy_day=self.is_holy_day,
                    sunset_start=sunset_start,
                    recurring_event=self
                )
                
                # Adiciona referências bíblicas
                event.biblical_references.set(self.biblical_references.all())
                
                return True
                
        except Exception as e:
            print(f"Erro ao criar evento para {event_date}: {str(e)}")
            raise e
