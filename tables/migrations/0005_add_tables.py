from django.db import migrations

def add_tables(apps, schema_editor):
    # Obtén el modelo de mesa
    Table = apps.get_model('tables', 'Table')

    # Define las posiciones de las mesas según tus especificaciones
    table_positions = [
      (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2),  # Mesas en Y2 desde X1 hasta X6
      (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4),  # Mesas en Y4 desde X1 hasta X6
      (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6),  # Mesas en Y6 desde X1 hasta X6
      (9, 2), (9, 3), (9, 4), (9, 5), (9, 6),          # Mesas en X9 desde Y2 hasta Y6
    ]

    # Insertar las mesas en la base de datos
    for x, y in table_positions:
        for i in range(1, 6):
            Table.objects.create(x_position=x, y_position=y, min_chairs=1, max_chairs=2, assigned_restaurant_id=i)

class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0004_alter_table_unique_together'),
    ]

    operations = [
        migrations.RunPython(add_tables),
    ]
