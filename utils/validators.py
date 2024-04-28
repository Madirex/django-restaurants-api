from django.core.exceptions import ValidationError

ALLOWED_ADDRESS_FIELDS = {
    "street",
    "number",
    "city",
    "province",
    "country",
    "postal_code",
}

def validate_address(address):
    if not isinstance(address, dict):
        raise ValidationError("La dirección debe ser un objeto JSON.")

    unexpected_fields = set(address.keys()) - ALLOWED_ADDRESS_FIELDS
    if unexpected_fields:
        raise ValidationError(f"Los siguientes campos no están permitidos: {', '.join(unexpected_fields)}")

    # Ahora puedes validar longitudes u otras restricciones
    max_lengths = {
        'street': 100,
        'number': 10,
        'city': 50,
        'province': 50,
        'country': 50,
        'postal_code': 10,
    }

    # Validar que todos los campos sean strings y que no excedan la longitud máxima
    for field, max_length in max_lengths.items():
        if field in address:
            if not isinstance(address[field], str):
                raise ValidationError(f"El campo '{field}' debe ser una cadena de texto.")
            if len(address[field]) > max_length:
                raise ValidationError(f"El campo '{field}' no debe exceder {max_length} caracteres.")

    return address

def validate_half_hour(time_list):
    for t in time_list:
        # Asegurarse de que el minuto sea 0 o 30 y los segundos sean 0
        if t.minute not in [0, 30] or t.second != 0:
            raise ValidationError(
                "Las horas de apertura deben ser cada media hora y con segundos igual a 0 (por ejemplo, 8:00, 8:30, 9:00, etc.)."
            )

def validate_unique_schedule_day(schedule_queryset, day, schedule_id=None):
    """Valida que no haya un Schedule con el mismo día para el mismo Calendar"""
    if not schedule_queryset:
        raise ValidationError("El queryset proporcionado está vacío o es incorrecto.")

    existing_schedule = schedule_queryset.filter(day=day).exclude(id=schedule_id).first()

    #log de
    if existing_schedule and existing_schedule.day:
        raise ValidationError(
            f"Ya existe un horario para el día {existing_schedule} en este calendario."
        )
