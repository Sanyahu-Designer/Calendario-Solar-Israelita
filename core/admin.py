from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import path
from django.shortcuts import render
from django import forms
from datetime import datetime, timedelta
from .models import Event, BiblicalReference, SolarDate, EventType, RecurringEvent, SolarTimes

class SolarDateBulkUploadForm(forms.Form):
    start_date = forms.DateField(
        label='Data Inicial',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    end_date = forms.DateField(
        label='Data Final',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    initial_solar_day = forms.IntegerField(
        label='Dia Solar Inicial',
        min_value=1,
        max_value=30
    )
    initial_solar_month = forms.ChoiceField(
        label='Mês Solar Inicial',
        choices=[
            ('Primeiro mês', 'Primeiro mês'),
            ('Segundo mês', 'Segundo mês'),
            ('Terceiro mês', 'Terceiro mês'),
            ('Quarto mês', 'Quarto mês'),
            ('Quinto mês', 'Quinto mês'),
            ('Sexto mês', 'Sexto mês'),
            ('Sétimo mês', 'Sétimo mês'),
            ('Oitavo mês', 'Oitavo mês'),
            ('Nono mês', 'Nono mês'),
            ('Décimo mês', 'Décimo mês'),
            ('Décimo primeiro mês', 'Décimo primeiro mês'),
            ('Décimo segundo mês', 'Décimo segundo mês'),
        ]
    )

# Register your models here.

class BiblicalReferenceInline(admin.TabularInline):
    model = BiblicalReference
    extra = 1

@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color', 'icon')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(SolarDate)
class SolarDateAdmin(admin.ModelAdmin):
    list_display = ('gregorian_date', 'get_display_date', 'is_extra_day')
    list_filter = ('is_extra_day', 'solar_month')
    search_fields = ('gregorian_date', 'solar_month')
    ordering = ('gregorian_date',)
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'bulk-upload/',
                self.admin_site.admin_view(self.bulk_upload_view),
                name='solar-date-bulk-upload',
            ),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['bulk_upload_url'] = 'bulk-upload/'
        return super().changelist_view(request, extra_context=extra_context)

    def bulk_upload_view(self, request):
        if request.method == 'POST':
            form = SolarDateBulkUploadForm(request.POST)
            if form.is_valid():
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
                solar_day = form.cleaned_data['initial_solar_day']
                solar_month = form.cleaned_data['initial_solar_month']
                
                # Lista de meses solares em ordem
                solar_months = [
                    'Primeiro mês', 'Segundo mês', 'Terceiro mês', 'Quarto mês',
                    'Quinto mês', 'Sexto mês', 'Sétimo mês', 'Oitavo mês',
                    'Nono mês', 'Décimo mês', 'Décimo primeiro mês', 'Décimo segundo mês'
                ]
                
                current_date = start_date
                current_solar_day = solar_day
                current_solar_month = solar_month
                month_idx = solar_months.index(current_solar_month)
                
                while current_date <= end_date:
                    # Primeiro remove qualquer data solar existente para esta data gregoriana
                    SolarDate.objects.filter(gregorian_date=current_date).delete()
                    
                    # Cria a nova data solar
                    SolarDate.objects.create(
                        gregorian_date=current_date,
                        solar_day=current_solar_day,
                        solar_month=current_solar_month
                    )
                    
                    # Incrementa o dia solar
                    current_solar_day += 1
                    if current_solar_day > 30:
                        current_solar_day = 1
                        month_idx = (month_idx + 1) % len(solar_months)
                        current_solar_month = solar_months[month_idx]
                    
                    current_date += timedelta(days=1)
                
                self.message_user(request, 'Datas solares cadastradas com sucesso!')
                return HttpResponseRedirect('../')
        else:
            form = SolarDateBulkUploadForm()
        
        context = {
            'form': form,
            'title': 'Cadastro em Lote de Datas Solares',
            'opts': self.model._meta,
        }
        return render(request, 'admin/solar_date_bulk_upload.html', context)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'gregorian_date', 'event_type', 'event_type_new', 'is_holy_day', 'sunset_start')
    list_filter = ('event_type', 'event_type_new', 'is_holy_day', 'sunset_start')
    search_fields = ('title', 'description')
    autocomplete_fields = ['solar_date']
    filter_horizontal = ('biblical_references',)
    date_hierarchy = 'gregorian_date'
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('title', 'description')
        }),
        ('Datas', {
            'fields': ('gregorian_date', 'solar_date')
        }),
        ('Tipo de Evento', {
            'fields': ('event_type', 'event_type_new')
        }),
        ('Configurações', {
            'fields': ('is_holy_day', 'sunset_start')
        }),
        ('Referências', {
            'fields': ('biblical_references',)
        }),
    )

    def save_model(self, request, obj, form, change):
        # Salva o modelo
        super().save_model(request, obj, form, change)
        
        # Se este evento foi gerado por um evento recorrente, atualiza apenas este evento
        if obj.recurring_event and change:
            obj.save()

@admin.register(BiblicalReference)
class BiblicalReferenceAdmin(admin.ModelAdmin):
    list_display = ('book', 'chapter', 'verse', 'text')
    list_filter = ('book',)
    search_fields = ('book', 'text')
    ordering = ('book', 'chapter', 'verse')

@admin.register(RecurringEvent)
class RecurringEventAdmin(admin.ModelAdmin):
    class Media:
        js = ['core/js/recurring_event.js']
    
    list_display = ['title', 'recurrence_type', 'start_date', 'end_date', 'is_holy_day', 'sunset_start']
    actions = ['generate_events_action']
    list_filter = ['recurrence_type', 'event_type', 'is_holy_day']
    search_fields = ['title', 'description']
    filter_horizontal = ['biblical_references']
    
    fieldsets = [
        (None, {
            'fields': ['title', 'description', 'recurrence_type']
        }),
        ('Configuração da Recorrência', {
            'fields': [
                ('weekday',),
                ('annual_month', 'annual_day'),
            ],
            'classes': ['collapse']
        }),
        ('Configurações do Evento', {
            'fields': [
                'event_type',
                'event_type_new',
                'is_holy_day',
                'sunset_start',
                'biblical_references'
            ]
        }),
        ('Período', {
            'fields': [('start_date', 'end_date')]
        })
    ]
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        try:
            # Gera eventos para o próximo ano após salvar
            events_created = obj.generate_events()
            if events_created > 0:
                self.message_user(
                    request,
                    f"{events_created} eventos foram gerados com sucesso para '{obj.title}'."
                )
            else:
                self.message_user(
                    request,
                    "Nenhum novo evento foi gerado. Verifique se as datas solares correspondentes existem.",
                    level=messages.WARNING
                )
        except Exception as e:
            self.message_user(
                request,
                f"Erro ao gerar eventos: {str(e)}",
                level=messages.ERROR
            )

    def generate_events_action(self, request, queryset):
        total_events = 0
        skipped_dates = 0
        
        for recurring_event in queryset:
            try:
                events_created = recurring_event.generate_events()
                total_events += events_created
            except Exception as e:
                self.message_user(
                    request,
                    f"Erro ao gerar eventos para '{recurring_event.title}': {str(e)}",
                    level=messages.ERROR
                )
                continue
        
        if total_events > 0:
            self.message_user(
                request,
                f'Foram gerados {total_events} eventos com sucesso.',
                messages.SUCCESS
            )
        else:
            self.message_user(
                request,
                'Nenhum novo evento foi gerado. Verifique se as datas solares correspondentes existem.',
                messages.WARNING
            )
    
    generate_events_action.short_description = "Gerar eventos para os itens selecionados"

@admin.register(SolarTimes)
class SolarTimesAdmin(admin.ModelAdmin):
    list_display = ('date', 'sunrise', 'solar_noon', 'sunset', 'latitude', 'longitude')
    list_filter = ('date',)
    search_fields = ('date',)
    date_hierarchy = 'date'
    ordering = ('-date',)
