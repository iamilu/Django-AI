from django.db import models
from category.models import Category
from accounts.models import Account
from django.urls import reverse

import math

# Create your models here.

'''
write a Product model to store information related to product with fields name
product_name, slug, description, price, image, stock, created_date, modified_date and category as foreign key
'''
class Product(models.Model):
    product_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.FloatField()
    image = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name
    
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
    
    '''
    get average rating of the product
    '''
    @property
    def avgRating(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=models.Avg('rating'))
        avg = 0
        if reviews:
            avg = float(reviews['average'])
        
        if avg < 0.5:
            avg = math.floor(avg)
        elif avg > 0.5:
            avg = math.ceil(avg)
        if avg < 1.5:
            avg = math.floor(avg)
        elif avg > 1.5:
            avg = math.ceil(avg)
        if avg < 2.5:
            avg = math.floor(avg)
        elif avg > 2.5:
            avg = math.ceil(avg)
        if avg < 3.5:
            avg = math.floor(avg)
        elif avg > 3.5:
            avg = math.ceil(avg)
        if avg < 4.5:
            avg = math.floor(avg)
        elif avg > 4.5:
            avg = math.ceil(avg)

        return avg
    
    '''
    get total review count of the product
    '''
    @property
    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=models.Count('id'))
        total = 0
        if reviews:
            total = int(reviews['count'])
        return total

'''
write a Product Gallery model to store information related to product gallery with fields name
product as foreign key and image
'''
class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    image = models.ImageField(upload_to='photos/products/gallery', blank=True)

    '''
    write a class Meta to change the verbose name to Product Galleries
    '''
    class Meta:
        verbose_name = 'Product Gallery'
        verbose_name_plural = 'Product Galleries'

    def __str__(self):
        return self.product.product_name

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)

'''
write a variation category choice based on colors and sizes
'''
variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)

'''
write a Variation model to store information related to product variation with fields names
product as foreign key and variation_category from given choice, variation_value, is_active and created_date
'''
class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=50, choices=variation_category_choice)
    variation_value = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value

'''
write a Review Rating model to store information related to product review with fields name
product as foreign key and user as foreign key, subject, review, rating, ip, status, created_at and updated_at
'''
class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    '''
    write a class Meta to change the verbose name to Review Ratings
    '''
    class Meta:
        verbose_name = 'Review Rating'
        verbose_name_plural = 'Review Ratings'

    def __str__(self):
        return self.review