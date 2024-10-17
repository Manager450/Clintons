from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator
from .forms import CustomUserCreationForm

def index(request):
    return render(request, 'shop/index.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'shop/signup.html', {'form': form})


# Check if the user is admin
def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'shop/admin_dashboard.html')

@user_passes_test(is_admin)
def manage_products(request):
    products = Product.objects.all()
    return render(request, 'shop/manage_products.html', {'products': products})

@user_passes_test(is_admin)
def manage_orders(request):
    orders = Order.objects.filter(shipped=False)
    return render(request, 'shop/manage_orders.html', {'orders': orders})

@user_passes_test(is_admin)
def order_list(request):
    orders = Order.objects.all()  # Adjust this query as necessary
    return render(request, 'shop/order_list.html', {'orders': orders})

@user_passes_test(is_admin)
def user_list(request):
    users = User.objects.all()  # Adjust this query as necessary
    return render(request, 'shop/user_list.html', {'users': users})

@user_passes_test(is_admin)
def add_product(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        image = request.FILES['image']
        stock = request.POST['stock']
        Product.objects.create(name=name, description=description, price=price, image=image, stock=stock)
        return redirect('manage_products')
    return render(request, 'shop/add_product.html')


# Add to cart
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order, created = Order.objects.get_or_create(user=request.user, product=product, shipped=False)
    order.quantity += 1
    order.total_price = order.quantity * product.price
    order.save()
    return redirect('cart')

# View cart
def cart(request):
    orders = Order.objects.filter(user=request.user, shipped=False)
    total = sum(order.total_price for order in orders)
    return render(request, 'shop/cart.html', {'orders': orders, 'total': total})

# Checkout process
def checkout(request):
    orders = Order.objects.filter(user=request.user, shipped=False)
    if request.method == 'POST':
        for order in orders:
            order.shipped = True
            order.save()
        return redirect('order_confirmation')
    return render(request, 'shop/checkout.html', {'orders': orders})

def order_confirmation(request):
    return render(request, 'shop/order_confirmation.html')



def send_order_confirmation(user):
    subject = 'Order Confirmation'
    message = 'Thank you for your order. Your tracking number is XYZ123.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, email_from, recipient_list)

def product_list(request):
    products = Product.objects.all()
    paginator = Paginator(products, 10)  # 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'shop/product_list.html', {'page_obj': page_obj})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})



