from django.db import migrations

def add_restaurants(apps, schema_editor):
    # Obtén el modelo de restaurante
    Restaurant = apps.get_model('restaurants', 'Restaurant')

    # Nombres de los restaurantes
    restaurant_names = [
        "MadiRestaurant",
        "Delicia Urbana",
        "Sabor Divino",
        "GastroLab",
        "Rincón del Sabor",
        "Estrella Gastronómica",
        "Bocado Celestial"
    ]

    # Insertar los restaurantes en la base de datos
    for name in restaurant_names:
        Restaurant.objects.create(name=name)

class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_restaurants),
    ]