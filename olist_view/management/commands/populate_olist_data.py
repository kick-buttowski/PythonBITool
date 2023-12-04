from olist_view.management.commands.data_population_utils import load_data
from olist_view.models import Customer, Geolocation, OrderItem, OrderPayment, OrderReview, Order, Seller, \
    ProductTranslation, Product, Alias


def load_olist_data(cls):
    geolocation_csv_path = 'datasets/olist_geolocation_dataset.csv'
    load_data(cls, Geolocation, geolocation_csv_path, {}, {})

    products_csv_path = 'datasets/olist_products_dataset.csv'
    load_data(cls, Product, products_csv_path, {}, {})

    product_translation_csv_path = 'datasets/product_category_name_translation.csv'
    load_data(cls, ProductTranslation, product_translation_csv_path, {}, {})

    aliases_csv_path = 'datasets/olist_aliases.csv'
    load_data(cls, Alias, aliases_csv_path, {}, {})

    customers_csv_path = 'datasets/olist_customers_dataset.csv'
    load_data(cls, Customer, customers_csv_path, {"zip_code_prefix": Geolocation},
              {"zip_code_prefix": "zip_code_prefix"})

    orders_csv_path = 'datasets/olist_orders_dataset.csv'
    load_data(cls, Order, orders_csv_path, {"customer_id": Customer}, {"customer_id": "customer_id"})

    sellers_csv_path = 'datasets/olist_sellers_dataset.csv'
    load_data(cls, Seller, sellers_csv_path, {"zip_code_prefix": Geolocation},
              {"zip_code_prefix": "zip_code_prefix"})

    order_items_csv_path = 'datasets/olist_order_items_dataset.csv'
    load_data(cls, OrderItem, order_items_csv_path, {"order_id": Order,
                                                "product_id": Product,
                                                "seller_id": Seller},
              {"order_id": "order_id", "product_id": "product_id",
               "seller_id": "seller_id"})

    order_payments_csv_path = 'datasets/olist_order_payments_dataset.csv'
    load_data(cls, OrderPayment, order_payments_csv_path, {"order_id": Order}, {"order_id": "order_id"})

    order_reviews_csv_path = 'datasets/olist_order_reviews_dataset.csv'
    load_data(cls, OrderReview, order_reviews_csv_path, {"order_id": Order}, {"order_id": "order_id"})
