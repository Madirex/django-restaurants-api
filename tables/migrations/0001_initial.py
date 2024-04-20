# Generated by Django 3.2.4 on 2024-04-20 17:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x_position', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('y_position', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('min_chairs', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('max_chairs', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('reserved', models.BooleanField(default=False)),
                ('reserved_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]