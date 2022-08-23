# Generated by Django 4.0.5 on 2022-08-23 18:28

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music_api', '0005_alter_music_added_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='audio',
            field=cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='audio'),
        ),
        migrations.AlterField(
            model_name='music',
            name='img',
            field=cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='img'),
        ),
    ]