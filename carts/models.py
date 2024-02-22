from django.db import models
from accounts.models import Account
from store.models import Product, Variation

# Create your models here.
'''
write a Cart model to store inforamtion about cart with fields name
cart_id and date_added
'''
class Cart(models.Model):
    cart_id = models.CharField(max_length=100, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

'''
write a Cart Item model to store information about cart items with fields name
user as foreign key, cart as foreign key, product as foreign key, variation as many to many relationship, quantity and is_active
'''
class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    '''
    write a Meta class to change the verbose name to Cart Items
    '''
    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'

    def __unicode__(self):
        return self.product
    
    def sub_total(self):
        return self.product.price * self.quantity