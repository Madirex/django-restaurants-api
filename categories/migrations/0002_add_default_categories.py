from django.db import migrations

def add_default_categories(apps, schema_editor):
    # Obtén el modelo que necesitas
    Category = apps.get_model('categories', 'Category')

    # Inserta las categorías por defecto
    categories = [
        'Carne',
        'Postre',
        'Pescado',
        'Vegetariano',
        'Vegano',
        'Bebida azucarada',
        'Bebida sin azúcar',
        'Bebida fría'
    ]

    for category_name in categories:
        Category.objects.create(name=category_name)

class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_default_categories),
    ]
