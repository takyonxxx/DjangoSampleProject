# Generated by Django 4.2.6 on 2023-11-06 12:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testApp', '0004_delete_vipcustomer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='product',
            new_name='ordered_product',
        ),
    ]
