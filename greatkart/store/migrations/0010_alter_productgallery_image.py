# Generated by Django 5.1 on 2024-11-23 08:13

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_alter_product_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productgallery',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
    ]