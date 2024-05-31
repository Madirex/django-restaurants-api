from django.db import migrations

def add_dishes(apps, schema_editor):
    # Obtén el modelo de plato
    Dish = apps.get_model('dishes', 'Dish')

    # Lista de platos de prueba
    dishes = [
        {
            "name": "Ensalada César",
            "description": "Ensalada de lechuga romana con aderezo César, crutones y queso parmesano.",
            "price": 8.99,
            "dish_type": "APPETIZER",
            "ingredients": ["Lechuga", "Aderezo César", "Crutones", "Queso parmesano", "Pollo (opcional)"],
            "calories": 250,
            "image": "dishes_examples/ensalada_cesar.bmp",
            "preparation_time": 10,
            "category": "Vegetariano",
            "is_active": True,
        },
        {
            "name": "Filete de Res",
            "description": "Jugoso filete de res a la parrilla con guarnición de vegetales.",
            "price": 19.99,
            "dish_type": "MAIN_COURSE",
            "ingredients": ["Filete de res", "Vegetales", "Especias"],
            "calories": 600,
            "image": "dishes_examples/filete_res.bmp",
            "preparation_time": 25,
            "category": "Carne",
            "is_active": True,
        },
        {
            "name": "Tarta de Queso",
            "description": "Deliciosa tarta de queso con base de galleta y cobertura de frutas.",
            "price": 5.99,
            "dish_type": "DESSERT",
            "ingredients": ["Queso crema", "Galleta", "Azúcar", "Frutas"],
            "calories": 400,
            "image": "dishes_examples/tarta_queso.bmp",
            "preparation_time": 15,
            "category": "Postre",
            "is_active": True,
        },
        {
            "name": "Limonada",
            "description": "Refrescante limonada casera con hielo.",
            "price": 2.99,
            "dish_type": "DRINK",
            "ingredients": ["Limón", "Agua", "Azúcar", "Hielo"],
            "calories": 90,
            "image": "dishes_examples/limonada.bmp",
            "preparation_time": 5,
            "category": "Bebida fría",
            "is_active": True,
        },
    ]

    # Insertar los platos en la base de datos
    for dish_data in dishes:
        Dish.objects.create(**dish_data)

class Migration(migrations.Migration):

    dependencies = [
        ('dishes', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_dishes),
    ]
