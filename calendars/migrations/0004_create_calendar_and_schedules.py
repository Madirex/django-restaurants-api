from datetime import datetime, timedelta
from django.db import migrations

def create_calendar_and_schedules(apps, schema_editor):
    for i in range(1, 8):

        # Obtén los modelos que necesitas
        Calendar = apps.get_model('calendars', 'Calendar')
        Schedule = apps.get_model('schedules', 'Schedule')
        Restaurant = apps.get_model('restaurants', 'Restaurant')

        # Busca el restaurante 1 (o el que corresponda)
        restaurant = Restaurant.objects.get(id=i)  # Reemplaza 1 con el ID correcto de tu restaurante

        # Define las fechas de inicio y fin para cada tipo de horario
        winter_start = datetime(2024, 1, 1)
        winter_end = datetime(2024, 3, 31)
        summer_start = datetime(2024, 6, 1)
        summer_end = datetime(2024, 8, 31)

        # Crea el calendario para el restaurante con las fechas definidas
        restaurant_calendar = Calendar.objects.create(
            normal_start_date=winter_end,
            summer_start_date=summer_start,
            winter_start_date=winter_start
        )

        # Define las horas abiertas para cada tipo de horario
        winter_hours = generate_hours(datetime.strptime('09:00', '%H:%M'), datetime.strptime('21:00', '%H:%M'))
        summer_hours = generate_hours(datetime.strptime('09:00', '%H:%M'), datetime.strptime('22:00', '%H:%M'))
        normal_hours = generate_hours(datetime.strptime('09:00', '%H:%M'), datetime.strptime('20:00', '%H:%M'))

        # Crea los horarios en la base de datos
        winter_schedule = Schedule.objects.create(calendar=restaurant_calendar, day=winter_start, opened_hours=winter_hours)
        summer_schedule = Schedule.objects.create(calendar=restaurant_calendar, day=summer_start, opened_hours=summer_hours)
        normal_schedule = Schedule.objects.create(calendar=restaurant_calendar, day=winter_end, opened_hours=normal_hours)

        # Asigna los horarios al calendario del restaurante
        restaurant_calendar.winter_week_schedule = winter_schedule
        restaurant_calendar.summer_week_schedule = summer_schedule
        restaurant_calendar.normal_week_schedule = normal_schedule

        # Guarda los cambios en la base de datos
        restaurant_calendar.save()

        # Ahora asignar el calendario al restaurante
        restaurant.calendar = restaurant_calendar

        # Guardar restaurante
        restaurant.save()

def generate_hours(start, end):
    hours = []
    current_time = start
    while current_time < end:
        hours.append(current_time)
        current_time += timedelta(minutes=30)
    return hours

class Migration(migrations.Migration):

    dependencies = [
        ('calendars', '0003_auto_20240428_1748'),
        ('schedules', '0003_alter_schedule_day'),
        ('restaurants', '0002_add_restaurants'),
    ]

    operations = [
        migrations.RunPython(create_calendar_and_schedules),
    ]
