from django.apps import AppConfig


class OrderLinesConfig(AppConfig):
    """Configuración de líneas de pedido."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'order_lines'
