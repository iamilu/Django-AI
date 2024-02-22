'''
write a store view to grab all products based on category slug name, if category slug is not None, else grab all products and pass it to the store.html page as context
'''
from django.shortcuts import render, redirect
from .models import Product, ProductGallery, ReviewRating
from .forms import ReviewForm
from category.models import Category
from carts.models import Cart, CartItem
from orders.models import OrderProduct
from carts.views import get_cart_id
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages

def store(request, category_slug=None):
    categories = None
    products = None
    if category_slug != None:
        categories = Category.objects.filter(slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
    else:
        products = Product.objects.all().filter(is_available=True)
    product_count = products.count()

    '''
    use paginator to diplay 10 products per page
    '''
    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    context = {
        'products': paged_products,
        'products_count': product_count
    }
    return render(request, 'store/store.html', context)

'''
write a view product_detail to grab product details based on category slug and product slug
'''
def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        
        '''
        check if the product is added to the cart, by the user if the user is authenticated or by the session id
        '''
        if request.user.is_authenticated:
            is_product_in_cart = CartItem.objects.filter(user=request.user, product=single_product).exists()
        else:
            cart = Cart.objects.get(cart_id=get_cart_id(request))
            is_product_in_cart = CartItem.objects.filter(cart=cart, product=single_product).exists()

        '''
        check if user has any ordered product if the user is authenticated or by the session id
        '''
        if request.user.is_authenticated:
            try:
                order_product = OrderProduct.objects.filter(user=request.user, product=single_product).exists()
            except OrderProduct.DoesNotExist:
                order_product = None
        else:
            order_product = None

        '''
        get product gallery details of the product
        '''
        product_gallery = ProductGallery.objects.filter(product=single_product)

        '''
        get review rating details of the product
        '''
        reviews = ReviewRating.objects.filter(product=single_product)
        for review in reviews:
            review.get_profile_pic_url = review.user.get_profile_pic(review.user)

    except Exception as e:
        raise e
    context = {
        'single_product': single_product,
        'is_product_in_cart': is_product_in_cart,
        'order_product': order_product,
        'product_gallery': product_gallery,
        'reviews': reviews,
    }
    return render(request, 'store/product_detail.html', context)

'''
write a search view to search products based on product name and description from query string
'''
def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'products_count': product_count
    }
    return render(request, 'store/store.html', context)

'''
write a submit_review view to update the review, if already present, else add a newreview for the product using ReviewForm based on product id
'''
def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    prodcut = Product.objects.get(id=product_id)

    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user=request.user, product=prodcut)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Your review has been updated successfully')
        except:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user = request.user
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted successfully')
            else:
                messages.error(request, 'Your review has not been submitted successfully')

    return redirect(url)
