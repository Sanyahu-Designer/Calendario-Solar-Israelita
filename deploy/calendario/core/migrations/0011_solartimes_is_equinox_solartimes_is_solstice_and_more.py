# Generated by Django 5.0 on 2025-01-14 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_solartimes'),
    ]

    operations = [
        migrations.AddField(
            model_name='solartimes',
            name='is_equinox',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='solartimes',
            name='is_solstice',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='solartimes',
            name='season_type',
            field=models.CharField(blank=True, choices=[('spring_equinox', 'Equinócio de Primavera'), ('summer_solstice', 'Solstício de Verão'), ('autumn_equinox', 'Equinócio de Outono'), ('winter_solstice', 'Solstício de Inverno')], max_length=20, null=True),
        ),
    ]