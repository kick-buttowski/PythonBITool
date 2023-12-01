from django.db import models


class Product(models.Model):
    product_id = models.CharField(max_length=32, unique=True)
    product_category_name = models.CharField(max_length=255)
    product_name_length = models.IntegerField(blank=True, null=True)
    product_description_length = models.IntegerField(blank=True, null=True)
    product_photos_qty = models.IntegerField(blank=True, null=True)
    product_weight_g = models.IntegerField(blank=True, null=True)
    product_length_cm = models.IntegerField(blank=True, null=True)
    product_height_cm = models.IntegerField(blank=True, null=True)
    product_width_cm = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"product: {self.product_id}"


class Customer(models.Model):
    customer_id = models.CharField(max_length=32, unique=True)
    customer_unique_id = models.CharField(max_length=32)
    zip_code_prefix = models.CharField(max_length=10)
    customer_city = models.CharField(max_length=255)
    customer_state = models.CharField(max_length=2)

    def __str__(self):
        return f"customer: {self.customer_id}"


class Geolocation(models.Model):
    zip_code_prefix = models.IntegerField(blank=True, null=True)
    geolocation_lat = models.FloatField()
    geolocation_lng = models.FloatField()
    geolocation_city = models.CharField(max_length=255)
    geolocation_state = models.CharField(max_length=2)

    def __str__(self):
        return f"geolocation: {self.zip_code_prefix} {self.geolocation_city} {self.geolocation_state}"


class OrderItem(models.Model):
    order_id = models.CharField(max_length=32)
    order_item_id = models.IntegerField(blank=True, null=True)
    product_id = models.CharField(max_length=32)
    seller_id = models.CharField(max_length=32)
    shipping_limit_date = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    freight_value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"orderitem: {self.order_id} {self.product_id}"


class OrderPayment(models.Model):
    order_id = models.CharField(max_length=32)
    payment_sequential = models.IntegerField(blank=True, null=True)
    payment_type = models.CharField(max_length=20)
    payment_installments = models.IntegerField(blank=True, null=True)
    payment_value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"orderpayment: {self.order_id} {self.payment_sequential} {self.payment_type}"


class OrderReview(models.Model):
    review_id = models.CharField(max_length=32)
    order_id = models.CharField(max_length=32)
    review_score = models.IntegerField(blank=True, null=True)
    review_comment_title = models.CharField(max_length=255, blank=True, null=True)
    review_comment_message = models.TextField(blank=True, null=True)
    review_creation_date = models.DateTimeField()
    review_answer_timestamp = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"orderreview: {self.review_id}"


class Order(models.Model):
    order_id = models.CharField(max_length=32, unique=True)
    customer_id = models.CharField(max_length=32)
    order_status = models.CharField(max_length=20)
    order_purchase_timestamp = models.DateTimeField(blank=True, null=True)
    order_approved_at = models.DateTimeField(null=True, blank=True)
    order_delivered_carrier_date = models.DateTimeField(null=True, blank=True)
    order_delivered_customer_date = models.DateTimeField(null=True, blank=True)
    order_estimated_delivery_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"order: {self.order_id}"


class Seller(models.Model):
    seller_id = models.CharField(max_length=32, unique=True)
    zip_code_prefix = models.CharField(max_length=10)
    seller_city = models.CharField(max_length=255)
    seller_state = models.CharField(max_length=2)

    def __str__(self):
        return f"seller: {self.seller_id} {self.seller_city}"


class ProductTranslation(models.Model):
    product_category_name = models.CharField(max_length=255, unique=True)
    product_category_name_english = models.CharField(max_length=255)

    def __str__(self):
        return f"producttranslation: {self.product_category_name}"


class Alias(models.Model):
    aliases = models.CharField(max_length=255, unique=True)
    column_name = models.CharField(max_length=255, null=False)
    table_name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return f"{self.aliases} {self.column_name}"
