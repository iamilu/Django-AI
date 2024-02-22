from django.contrib import admin
from .models import Payment, Order, OrderProduct

# Register your models here.
'''
write a OrderProductInline class
'''
class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment', 'user', 'product', 'variation', 'quantity', 'product_price', 'is_ordered', 'created_at')
    extra = 0

'''
write a OrderAdmin class
'''
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'email', 'order_total', 'status', 'is_ordered', 'created_at']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'first_name', 'last_name']
    list_per_page = 20
    inlines = [OrderProductInline]

'''
write a PaymentAdmin class
'''
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'user', 'payment_method', 'amount_paid', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['payment_id']
    list_per_page = 20
    readonly_fields = ['payment_id', 'user', 'payment_method', 'amount_paid', 'status', 'created_at']

'''
write a OrderProductAdmin class
'''
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['order', 'payment', 'user', 'product', 'quantity', 'product_price', 'is_ordered', 'created_at']
    readonly_fields = ['order', 'payment', 'user', 'product', 'variation', 'quantity', 'product_price', 'is_ordered', 'created_at']

admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)