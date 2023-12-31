# Generated by Django 4.2.1 on 2023-08-28 10:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_customer_phone_worker_manager'),
    ]

    operations = [
        migrations.CreateModel(
            name='Imgs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='images/')),
                ('book', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.book')),
            ],
        ),
    ]
