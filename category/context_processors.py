from .models import Category

'''
write a function to select category as context processor
'''
def select_category(request):
    categories = Category.objects.all()
    return dict(categories=categories)