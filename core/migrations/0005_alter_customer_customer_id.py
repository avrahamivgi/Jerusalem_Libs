# Generated by Django 4.2.1 on 2023-07-03 19:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_customer_customer_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_id',
            field=models.IntegerField(unique=True, validators=[django.core.validators.RegexValidator(message='ID should be a 9-digit number.', regex='^\\d{9}$')]),
        ),
    ]
