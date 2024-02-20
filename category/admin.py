from django.contrib import admin
from .models import Category

# Register your models here.
'''
write a Category Admin class to prepopulate the slug field with the name of the category and list of diplay fields as category_name and slug
'''
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
    list_display = ('category_name','slug')

admin.site.register(Category, CategoryAdmin)