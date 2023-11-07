# Generated by Django 4.2.1 on 2023-08-30 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_remove_img_book_book_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='img',
        ),
        migrations.AddField(
            model_name='book',
            name='cover_img',
            field=models.ImageField(blank=True, null=True, upload_to='book_covers/'),
        ),
        migrations.DeleteModel(
            name='Img',
        ),
    ]
