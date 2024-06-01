from django.db import migrations

def add_dishes(apps, schema_editor):
    # Obtén el modelo de plato
    Dish = apps.get_model('dishes', 'Dish')

    # Lista de platos de prueba
    dishes = [
            {
                "name": "Filete de Salmón a la Parrilla",
                "description": "Filete de salmón fresco marinado en una mezcla de limón, eneldo y aceite de oliva, luego asado a la parrilla y servido con una salsa de mantequilla de limón.",
                "price": 16.99,
                "dish_type": "MAIN_COURSE",
                "ingredients": ["Filete de salmón", "Limón", "Eneldo", "Aceite de oliva", "Mantequilla", "Pimienta"],
                "calories": 450,
                "image": "dishes_examples/filete_salmon_parrilla.jpg",
                "preparation_time": 20,
                "category": "Pescado",
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
                "name": "Risotto de Champiñones",
                "description": "Risotto cremoso y reconfortante preparado con arroz Arborio, champiñones frescos, caldo de verduras y queso parmesano.",
                "price": 12.99,
                "dish_type": "MAIN_COURSE",
                "ingredients": ["Arroz Arborio", "Champiñones", "Caldo de verduras", "Cebolla", "Vino blanco", "Queso parmesano"],
                "calories": 450,
                "image": "dishes_examples/risotto_champinones.jpg",
                "preparation_time": 40,
                "category": "Italiano",
                "is_active": True,
            },
            {
                "name": "Pad Thai de Camarones",
                "description": "Clásico plato tailandés de fideos de arroz salteados con camarones, tofu, huevo, brotes de soja y cacahuetes, aderezado con una deliciosa salsa agridulce.",
                "price": 14.99,
                "dish_type": "MAIN_COURSE",
                "ingredients": ["Fideos de arroz", "Camarones", "Tofu", "Huevo", "Brotes de soja", "Cacahuetes", "Salsa de tamarindo"],
                "calories": 550,
                "image": "dishes_examples/pad_thai_camarones.jpg",
                "preparation_time": 35,
                "category": "Tailandés",
                "is_active": True,
            },
            {
                "name": "Chuletas de Cordero a la Parrilla",
                "description": "Tiernas chuletas de cordero marinadas con hierbas mediterráneas y ajo, asadas a la parrilla y servidas con una guarnición de verduras asadas y puré de patatas.",
                "price": 18.99,
                "dish_type": "MAIN_COURSE",
                "ingredients": ["Chuletas de cordero", "Hierbas mediterráneas", "Ajo", "Verduras", "Patatas"],
                "calories": 700,
                "image": "dishes_examples/chuletas_cordero_parrilla.jpg",
                "preparation_time": 45,
                "category": "Mediterráneo",
                "is_active": True,
            },
            {
                "name": "Pasta Alfredo con Pollo",
                "description": "Pasta fettuccine cocida al dente y mezclada con una cremosa salsa Alfredo de queso parmesano, servida con trozos de pollo a la parrilla y espolvoreada con perejil fresco.",
                "price": 13.99,
                "dish_type": "MAIN_COURSE",
                "ingredients": ["Pasta fettuccine", "Pollo", "Nata", "Queso parmesano", "Mantequilla", "Perejil"],
                "calories": 620,
                "image": "dishes_examples/pasta_alfredo_pollo.jpg",
                "preparation_time": 30,
                "category": "Italiano",
                "is_active": True,
            },
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
                "name": "Tartar de Salmón",
                "description": "Salmón fresco cortado en dados finos y marinado con limón, aceite de oliva, alcaparras y cebollín, servido con tostadas de pan crujiente.",
                "price": 12.99,
                "dish_type": "APPETIZER",
                "ingredients": ["Salmón fresco", "Limón", "Aceite de oliva", "Alcaparras", "Cebollín", "Pan crujiente"],
                "calories": 250,
                "image": "dishes_examples/tartar_salmon.jpg",
                "preparation_time": 20,
                "category": "Mariscos",
                "is_active": True,
            },
            {
                "name": "Carpaccio de Res",
                "description": "Finas láminas de solomillo de res marinadas en aceite de oliva, limón, parmesano y rúcula fresca, adornadas con escamas de sal marina.",
                "price": 14.99,
                "dish_type": "APPETIZER",
                "ingredients": ["Solomillo de res", "Aceite de oliva", "Limón", "Queso parmesano", "Rúcula", "Sal marina"],
                "calories": 280,
                "image": "dishes_examples/carpaccio_res.jpg",
                "preparation_time": 15,
                "category": "Italiano",
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
            {
                "name": "Piña Colada",
                "description": "Cóctel tropical cremoso de piña, ron y leche de coco, servido con hielo y decorado con una rodaja de piña y una cereza.",
                "price": 9.99,
                "dish_type": "DRINK",
                "ingredients": ["Piña", "Ron blanco", "Leche de coco", "Hielo", "Azúcar"],
                "calories": 250,
                "image": "dishes_examples/pina_colada.jpg",
                "preparation_time": 10,
                "category": "Cóctel",
                "is_active": True,
            },
            {
                "name": "Café Helado",
                "description": "Café negro recién preparado, enfriado y servido con hielo, ideal para una dosis refrescante de cafeína en días calurosos.",
                "price": 3.49,
                "dish_type": "DRINK",
                "ingredients": ["Café", "Hielo", "Azúcar (opcional)"],
                "calories": 10,
                "image": "dishes_examples/cafe_helado.jpg",
                "preparation_time": 5,
                "category": "Bebida fría",
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
                "name": "Tiramisú",
                "description": "Clásico postre italiano con capas de bizcocho empapado en café, mascarpone y cacao en polvo.",
                "price": 6.99,
                "dish_type": "DESSERT",
                "ingredients": ["Bizcocho", "Café", "Mascarpone", "Cacao en polvo", "Huevo"],
                "calories": 350,
                "image": "dishes_examples/tiramisu.jpg",
                "preparation_time": 20,
                "category": "Postre",
                "is_active": True,
            },
            {
                "name": "Brownie de Chocolate",
                "description": "Brownie de chocolate denso y húmedo, con trozos de nueces. Crujiente y sabroso.",
                "price": 4.99,
                "dish_type": "DESSERT",
                "ingredients": ["Chocolate", "Mantequilla", "Azúcar", "Huevo", "Harina", "Nueces"],
                "calories": 350,
                "image": "dishes_examples/brownie_chocolate.jpg",
                "preparation_time": 30,
                "category": "Postre",
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
