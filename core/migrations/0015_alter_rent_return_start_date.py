# Generated by Django 4.2.1 on 2023-07-10 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_rent_return_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='return_start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
