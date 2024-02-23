from django.contrib import admin
from .models import Product, ProductGallery, Variation, ReviewRating

import admin_thumbnails
# Register your models here.
'''
write a Product Gallery Inline class to display product gallery images as a thubnails in django admin page
'''
@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

'''
write a Product Admin class to prepopulate the slug field with the product name and list of display fields as product_name, price, stock, category, is_available and modified_date
'''
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    
    inlines = [ProductGalleryInline]

'''
write a Variation Admin class to display fields name such as product, variation_category, variation_value, is_active and to filter with fields name product, variation_category, variation_value
'''
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value')
    list_per_page = 10
    ordering = ('product', 'variation_category', 'variation_value')

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductGallery)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)