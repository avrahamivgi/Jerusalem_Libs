# Generated by Django 4.2.1 on 2023-08-29 08:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_rename_imgs_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='img',
            name='book',
        ),
        migrations.AddField(
            model_name='book',
            name='img',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.img'),
        ),
    ]
