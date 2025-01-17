# Generated by Django 5.0 on 2025-01-04 21:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_update_holy_day_verbose_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='recurring_event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='generated_events', to='core.recurringevent', verbose_name='Evento Recorrente'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(choices=[('festival', 'Festival Bíblico'), ('historical', 'Evento Histórico'), ('sabbath', 'Shabbat'), ('new_month', 'Rosh Chodesh'), ('equinox', 'Equinócio'), ('solstice', 'Solstício'), ('tekufah', 'Tekufah')], default='historical', max_length=20, verbose_name='Tipo de Evento'),
        ),
        migrations.AlterField(
            model_name='recurringevent',
            name='event_type',
            field=models.CharField(choices=[('festival', 'Festival Bíblico'), ('historical', 'Evento Histórico'), ('sabbath', 'Shabbat'), ('new_month', 'Rosh Chodesh'), ('equinox', 'Equinócio'), ('solstice', 'Solstício'), ('tekufah', 'Tekufah')], default='historical', max_length=20, verbose_name='Tipo de Evento'),
        ),
    ]
