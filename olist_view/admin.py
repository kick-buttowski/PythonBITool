from django.contrib import admin
from .models import (Product, Customer, Order, OrderItem, OrderReview,
                     OrderPayment, ProductTranslation, Geolocation, Seller, Alias, PublicDashboards)

admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderReview)
admin.site.register(OrderPayment)
admin.site.register(ProductTranslation)
admin.site.register(Geolocation)
admin.site.register(Seller)
admin.site.register(Alias)
admin.site.register(PublicDashboards)
