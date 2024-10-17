from django.urls import path, include
from shop import views

urlpatterns = [
    path('admin/', include('shop.urls')),
    path('accounts/', include('allauth.urls')), # Django Allauth
    path('', views.index, name='home'),
]
