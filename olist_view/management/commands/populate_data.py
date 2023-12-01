import csv
from django.core.management.base import BaseCommand
from olist_view.models import Customer, Geolocation, OrderItem, OrderPayment, OrderReview, Order, Seller, \
    ProductTranslation, Product, Alias


class Command(BaseCommand):
    help = 'Initialize data from CSV files into the database'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting data population...'))

        customers_csv_path = 'dataset_olist/olist_customers_dataset.csv'
        self.load_data(Customer, customers_csv_path)

        geolocation_csv_path = 'dataset_olist/olist_geolocation_dataset.csv'
        self.load_data(Geolocation, geolocation_csv_path)

        order_items_csv_path = 'dataset_olist/olist_order_items_dataset.csv'
        self.load_data(OrderItem, order_items_csv_path)

        order_payments_csv_path = 'dataset_olist/olist_order_payments_dataset.csv'
        self.load_data(OrderPayment, order_payments_csv_path)

        order_reviews_csv_path = 'dataset_olist/olist_order_reviews_dataset.csv'
        self.load_data(OrderReview, order_reviews_csv_path)

        products_csv_path = 'dataset_olist/olist_products_dataset.csv'
        self.load_data(Product, products_csv_path)

        sellers_csv_path = 'dataset_olist/olist_sellers_dataset.csv'
        self.load_data(Seller, sellers_csv_path)

        product_translation_csv_path = 'dataset_olist/product_category_name_translation.csv'
        self.load_data(ProductTranslation, product_translation_csv_path)

        orders_csv_path = 'dataset_olist/olist_orders_dataset.csv'
        self.load_data(Order, orders_csv_path)

        aliases_csv_path = 'dataset_olist/aliases.csv'
        self.load_data(Alias, aliases_csv_path)

        self.stdout.write(self.style.SUCCESS('Data loaded successfully.'))

    def load_data(self, model, csv_path):
        existing_count = model.objects.count()

        with open(csv_path, 'r', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            csv_count = len(rows)

            if existing_count < csv_count:
                new_data = rows[existing_count:]
                model.objects.bulk_create([model(**row) for row in new_data])
                self.stdout.write(self.style.SUCCESS(f'{len(new_data)} rows inserted for {model.__name__}.'))
            else:
                self.stdout.write(self.style.SUCCESS(f'No new data to insert for {model.__name__}.'))

