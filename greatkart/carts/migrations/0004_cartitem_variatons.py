# Generated by Django 5.1 on 2024-09-05 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0003_rename_product_cartitem_product'),
        ('store', '0003_rename_variation_value_variation_variation_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='variatons',
            field=models.ManyToManyField(blank=True, to='store.variation'),
        ),
    ]
