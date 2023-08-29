# Generated by Django 4.2.1 on 2023-07-06 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_rename_book_id_rent_book_book_return_period_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='return_period',
            field=models.IntegerField(choices=[(1, '10 days'), (2, '20 days'), (3, '30 days')], default=1),
        ),
    ]
