# Generated by Django 4.2.6 on 2023-11-06 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testApp', '0002_product_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
