# Generated by Django 3.2.4 on 2024-04-15 18:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CartCode',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('percent_discount', models.FloatField()),
                ('fixed_discount', models.FloatField()),
                ('available_uses', models.IntegerField()),
                ('expiration_date', models.DateTimeField()),
            ],
        ),
    ]
