from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Public-facing URLs
    path('', views.index, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/', views.order_confirmation, name='order_confirmation'),

    # Admin URLs
    path('manage-products/', views.manage_products, name='manage_products'),
    path('add-product/', views.add_product, name='add_product'),
    path('manage-orders/', views.manage_orders, name='manage_orders'),
    path('order-list/', views.order_list, name='order_list'),
    path('user-list/', views.user_list, name='user_list'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),  

    # Authentication URLs
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
