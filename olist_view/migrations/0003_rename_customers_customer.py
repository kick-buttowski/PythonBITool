# Generated by Django 4.2.7 on 2023-11-21 05:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('olist_view', '0002_customers_geolocation_orderitem_orderpayment_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Customers',
            new_name='Customer',
        ),
    ]