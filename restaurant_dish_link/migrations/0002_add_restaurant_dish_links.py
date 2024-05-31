from django.db import migrations

def link_dishes_to_restaurant(apps, schema_editor):
    # Obtén los modelos necesarios
    Restaurant = apps.get_model('restaurants', 'Restaurant')
    Dish = apps.get_model('dishes', 'Dish')
    RestaurantDishLink = apps.get_model('restaurant_dish_link', 'RestaurantDishLink')

    # Obtén todos los platos
    dishes = Dish.objects.all()

    # Enlazar cada plato con el restaurante
    for dish in dishes:
        for i in range(1, 8):
            RestaurantDishLink.objects.create(restaurant=Restaurant.objects.get(id=i), dish=dish, stock=10)

class Migration(migrations.Migration):

    dependencies = [
        ('restaurant_dish_link', '0001_initial'),
        ('restaurants', '0002_add_restaurants'),
        ('dishes', '0002_add_dishes'),
    ]

    operations = [
        migrations.RunPython(link_dishes_to_restaurant),
    ]
