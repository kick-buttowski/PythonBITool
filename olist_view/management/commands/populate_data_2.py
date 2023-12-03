import csv
from django.core.management.base import BaseCommand
from django.db.models.functions import datetime

from olist_view.models import Customer, Geolocation, OrderItem, OrderPayment, OrderReview, Order, Seller, \
    ProductTranslation, Product, Alias


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        model_data = {
            Geolocation: {
                "file": "dataset_olist/olist_geolocation_dataset.csv",
                "fk_fields": {},
            },
            Product: {
                "file": "dataset_olist/olist_products_dataset.csv",
                "fk_fields": {},
            },
            ProductTranslation: {
                "file": "dataset_olist/product_category_name_translation.csv",
                "fk_fields": {},
            },
            Alias: {
                "file": "dataset_olist/aliases.csv",
                "fk_fields": {},
            },
            Customer: {
                "file": "dataset_olist/olist_customers_dataset.csv",
                "fk_fields": {"customer_zip_code_prefix": Geolocation},
            },
            Order: {
                "file": "dataset_olist/olist_orders_dataset.csv",
                "fk_fields": {"customer_id": Customer},
            },
            Seller: {
                "file": "dataset_olist/olist_sellers_dataset.csv",
                "fk_fields": {"seller_zip_code_prefix": Geolocation},
            },
            OrderItem: {
                "file": "dataset_olist/olist_order_items_dataset.csv",
                "fk_fields": {"order_id": Order, "product_id": Product, "seller_id": Seller},
            },
            OrderPayment: {
                "file": "dataset_olist/olist_order_payments_dataset.csv",
                "fk_fields": {"order_id": Order},
            },
            OrderReview: {
                "file": "dataset_olist/olist_order_reviews_dataset.csv",
                "fk_fields": {"order_id": Order},
            },
        }

        for model_name, model_info in model_data.items():
            model = model_name
            existing_count = model.objects.count()
            file_path = model_info["file"]
            fk_lookup_fields = model_info.get("fk_fields", {})

            with open(file_path, "r") as f:
                reader = csv.reader(f)
                header = next(reader)
                rows = list(reader)
                csv_count = len(rows)

                if existing_count < csv_count:
                    new_data = rows[existing_count:]
                    for row in new_data:
                        try:
                            model_object = self.create_from_csv_row(model, row, fk_lookup_fields)
                            model_object.save()
                        except Exception as e:
                            print(f"Error creating {model_name} object from row: {row}. Error: {e}")
                    self.stdout.write(self.style.SUCCESS(f'{len(new_data)} rows inserted for {model.__name__}.'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'No new data to insert for {model.__name__}.'))

        print("Data population completed!")

    def create_from_csv_row(self, model, row, fk_lookup_fields=None):
        model_data = {}

        # Iterate through model fields and CSV columns
        for field, csv_index in zip(model._meta.get_fields(), range(len(row))):
            # Handle foreign key relationships
            if fk_lookup_fields and field.name in fk_lookup_fields:
                # Lookup foreign key object based on CSV value and assigned field
                fk_model = fk_lookup_fields[field.name]
                fk_value = row[csv_index]
                model_data[field.name] = fk_model.objects.get(
                    **{fk_model._meta.get_field(fk_lookup_fields[field.name]).name: fk_value})
            else:
                # Try converting to appropriate data type based on field type
                if field.get_internal_type() == "DateTimeField":
                    try:
                        model_data[field.name] = datetime.datetime.strptime(row[csv_index], "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        pass
                else:
                    model_data[field.name] = row[csv_index]

        return model(**model_data)
