from django.db import models
from accounts.models import Account
from store.models import Product, Variation

# Create your models here.
'''
write a Payment model with the following fields
user as foreign key, payment_id, payment_method, amount_paid, status and created_at
'''
class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id

'''
write a code to list down the choices for status field of Order model
'''
STATUS = (
    ('New', 'New'),
    ('Accepted', 'Accepted'),
    ('Completed', 'Completed'),
    ('Cancelled', 'Cancelled'),
    ('Pending', 'Pending'),
    ('Refunded', 'Refunded'),
    ('Shipped', 'Shipped'),
    ('Returned', 'Returned'),
    ('Processing', 'Processing'),
    ('Delivered', 'Delivered'),
    ('Paid', 'Paid'),
    ('Unpaid', 'Unpaid'),
)

'''
write a Order model with the following fields
user as foreign key, payment as foreign key, order_number, first_name, last_name, phone, email, address line 1, address line 2, city, pincode, state, country, status, order_note, order_toal, tax, ip, is_ordered, created_at and updated_at
'''
class Order(models.Model):
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=50, choices=STATUS, default='New')
    ip = models.CharField(max_length=50, blank=True)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_number
    
    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def full_address(self):
        return self.address_line_1 + ' ' + self.address_line_2

'''
write a Order Product model with the following fields
user as foreign key, payment as foreign key, order as foreign key, product as foreign key, variation as many to many relationship, product_price, quantity, is_ordered, created_at and updated_at
'''
class OrderProduct(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ManyToManyField(Variation, blank=True)
    product_price = models.FloatField()
    quantity = models.IntegerField()
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name