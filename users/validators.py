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
                raise ValueError(f"El campo '{field}' debe ser una cadena de texto.")
            if len(address[field]) > max_length:
                raise ValueError(f"El campo '{field}' no debe exceder {max_length} caracteres.")

    return address