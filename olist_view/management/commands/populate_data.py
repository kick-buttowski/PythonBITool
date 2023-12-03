import csv
from django.core.management.base import BaseCommand
from django.db import models
from datetime import datetime

from olist_view.models import Customer, Geolocation, OrderItem, OrderPayment, OrderReview, Order, Seller, \
    ProductTranslation, Product, Alias


class Command(BaseCommand):
    help = 'Initialize data from CSV files into the database'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting data population...'))

        geolocation_csv_path = 'dataset_olist/olist_geolocation_dataset.csv'
        self.load_data(Geolocation, geolocation_csv_path, {}, {})

        products_csv_path = 'dataset_olist/olist_products_dataset.csv'
        self.load_data(Product, products_csv_path, {}, {})

        product_translation_csv_path = 'dataset_olist/product_category_name_translation.csv'
        self.load_data(ProductTranslation, product_translation_csv_path, {}, {})

        aliases_csv_path = 'dataset_olist/aliases.csv'
        self.load_data(Alias, aliases_csv_path, {}, {})

        customers_csv_path = 'dataset_olist/olist_customers_dataset.csv'
        self.load_data(Customer, customers_csv_path, {"zip_code_prefix": Geolocation},
                       {"zip_code_prefix": "zip_code_prefix"})

        orders_csv_path = 'dataset_olist/olist_orders_dataset.csv'
        self.load_data(Order, orders_csv_path, {"customer_id": Customer}, {"customer_id": "customer_id"})

        sellers_csv_path = 'dataset_olist/olist_sellers_dataset.csv'
        self.load_data(Seller, sellers_csv_path, {"zip_code_prefix": Geolocation},
                       {"zip_code_prefix": "zip_code_prefix"})

        order_items_csv_path = 'dataset_olist/olist_order_items_dataset.csv'
        self.load_data(OrderItem, order_items_csv_path, {"orderitem_order_id": Order,
                                                         "orderitem_product_id": Product,
                                                         "orderitem_seller_id": Seller},
                       {"orderitem_order_id": "order_id", "orderitem_product_id": "product_id",
                        "orderitem_seller_id": "seller_id"})

        order_payments_csv_path = 'dataset_olist/olist_order_payments_dataset.csv'
        self.load_data(OrderPayment, order_payments_csv_path, {"order_id": Order}, {"order_id": "order_id"})

        order_reviews_csv_path = 'dataset_olist/olist_order_reviews_dataset.csv'
        self.load_data(OrderReview, order_reviews_csv_path, {"order_id": Order}, {"order_id": "order_id"})

        self.stdout.write(self.style.SUCCESS('Data loaded successfully.'))

    def load_data(self, model, csv_path, contains_fk, fk_map_pk):
        existing_count = model.objects.count()

        with open(csv_path, 'r', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            csv_count = len(rows)

            if existing_count < csv_count:
                new_data = rows[existing_count:]
                if len(contains_fk) > 0:
                    self.create_instances(model, new_data, contains_fk, fk_map_pk)
                else:
                    model.objects.bulk_create([model(**row) for row in new_data])
                self.stdout.write(self.style.SUCCESS(f'{len(new_data)} rows inserted for {model.__name__}.'))
            else:
                self.stdout.write(self.style.SUCCESS(f'No new data to insert for {model.__name__}.'))

    def create_instances(self, model, data, fk_fields, fk_map_pk):
        for row in data:
            to_insert = True
            for field in model._meta.fields:
                if isinstance(field, models.ForeignKey):
                    related_model = field.related_model
                    fk_value = row.pop(field.name)

                    try:
                        row[field.name] = fk_fields[field.name].objects.get(
                            **{fk_map_pk[field.name]: fk_value})
                    except related_model.DoesNotExist:
                        to_insert = False
                        self.stdout.write(self.style.WARNING(
                            f'Skipping row: {row}. {related_model.__name__} with {field.name}={fk_value} does not exist.'
                        ))
                        break
                elif field.get_internal_type() == "DateTimeField":
                    date_string = row.pop(field.name)
                    try:
                        datetime_object = datetime.strptime(date_string, '%Y-%m-%d')
                        row[field.name] = datetime_object.strftime('%Y-%m-%d')
                    except ValueError:
                        datetime_object = datetime.strptime(date_string, '%m/%d/%Y %H:%M')
                        row[field.name] = datetime_object.strftime('%Y-%m-%d')
            if to_insert:
                model.objects.create(**row)
