# Generated by Django 4.2.7 on 2023-12-03 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('olist_view', '0004_remove_orderitem_order_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer_id',
            field=models.ForeignKey(db_column='customer_id', on_delete=django.db.models.deletion.CASCADE, to='olist_view.customer'),
        ),
    ]
