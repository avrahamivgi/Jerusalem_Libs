# Generated by Django 4.2.1 on 2023-07-10 09:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_rent_return_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='return_start_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
