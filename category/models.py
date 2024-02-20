from django.db import models

# Create your models here.
'''
write a Category model to store information related to category with fields name
category_name, slug, description and category_image
'''
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(max_length=255, blank=True)
    category_image = models.ImageField(upload_to='photos/categories', blank=True)

    '''
    write a class Meta to change the verbose name to Categories
    '''
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name