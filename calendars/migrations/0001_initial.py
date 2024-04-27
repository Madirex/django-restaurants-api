# Generated by Django 3.2.4 on 2024-04-27 21:30

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('normal_week_schedule', models.DateField(help_text='Horario normal de la semana')),
                ('summer_week_schedule', models.DateField(help_text='Horario de verano')),
                ('winter_week_schedule', models.DateField(help_text='Horario de invierno')),
                ('normal_start_date', models.DateField(help_text='Fecha de inicio del horario normal')),
                ('summer_start_date', models.DateField(help_text='Fecha de inicio del horario de verano')),
                ('winter_start_date', models.DateField(help_text='Fecha de inicio del horario de invierno')),
                ('closed_days', django.contrib.postgres.fields.ArrayField(base_field=models.DateField(), default=list, help_text='Lista de días cerrados', size=None)),
            ],
        ),
    ]