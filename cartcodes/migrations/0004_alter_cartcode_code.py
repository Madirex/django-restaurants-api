# Generated by Django 3.2.4 on 2024-04-15 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartcodes', '0003_alter_cartcode_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartcode',
            name='code',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
