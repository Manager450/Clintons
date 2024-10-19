from django.urls import path, include
from shop import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', include('shop.urls')),
    path('accounts/', include('allauth.urls')), # Django Allauth
    path('', views.index, name='home'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
