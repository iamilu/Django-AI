from django.contrib import admin
from .models import Product, ProductGallery, Variation, ReviewRating

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductGallery)
admin.site.register(Variation)
admin.site.register(ReviewRating)