# Generated by Django 3.2.4 on 2024-04-15 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartcodes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartcode',
            name='expiration_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
