# Generated by Django 4.2.1 on 2023-07-17 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_library_book_lib_customer_lib_rent_lib'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='lib',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.library'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='lib',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.library'),
        ),
        migrations.AlterField(
            model_name='rent',
            name='lib',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.library'),
        ),
    ]