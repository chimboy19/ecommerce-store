# Generated by Django 5.1 on 2024-10-12 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('success', 'success'), ('Declined', 'Declined'), ('Accepted', 'Accepted'), ('Completed', 'Completed'), ('cancelled', 'Cancelled')], default='New', max_length=10),
        ),
    ]
