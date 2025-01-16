# Generated by Django 5.0 on 2025-01-13 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_add_recurring_event_to_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolarTimes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique=True)),
                ('sunrise', models.TimeField()),
                ('sunset', models.TimeField()),
                ('solar_noon', models.TimeField()),
                ('latitude', models.FloatField(default=-15.7801)),
                ('longitude', models.FloatField(default=-47.9292)),
            ],
            options={
                'verbose_name': 'Horário Solar',
                'verbose_name_plural': 'Horários Solares',
                'ordering': ['date'],
            },
        ),
    ]
