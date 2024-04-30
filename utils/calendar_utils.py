# your_django_app/utils/calendar_utils.py

from schedules.models import Schedule
from datetime import datetime
from reserves.models import Reserve
from datetime import timedelta
from rest_framework.exceptions import ValidationError

def get_schedule_for_day(calendar, day):
    # Lógica para obtener el Schedule para un día específico
    custom_schedule = Schedule.objects.filter(calendar=calendar, day=day).first()

    if custom_schedule:
        return custom_schedule

    # Determinar la estación y obtener el Schedule correspondiente
    if calendar.normal_start_date <= day < calendar.summer_start_date:
        schedule = calendar.normal_week_schedule
    elif calendar.summer_start_date <= day < calendar.winter_start_date:
        schedule = calendar.summer_week_schedule
    else:
        schedule = calendar.winter_week_schedule

    # Comprobar si el Schedule es null antes de devolverlo
    if schedule is None:
        raise ValidationError(f"No se encontró un horario para el día {day}")

    return schedule


def get_occupied_hours(reservations, opening_hours):
    occupied_hours = set()

    for reservation in reservations:
        start_reserve = reservation.start_reserve.time()
        finish_reserve = (reservation.finish_reserve - timedelta(minutes=5)).time()  # Restar 5 minutos

        for hour in opening_hours:
            time_hour = datetime.strptime(str(hour), "%H:%M:%S").time()

            if start_reserve <= time_hour < finish_reserve:  # Cambiar <= por <
                occupied_hours.add(str(hour))

    return occupied_hours


def get_available_hours(opening_hours, occupied_hours):
    # Lógica para obtener las horas disponibles
    return [str(hour) for hour in opening_hours if str(hour) not in occupied_hours]
