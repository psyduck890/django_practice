from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', include('django.contrib.auth.urls')),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    # path('login/', include('core.urls')),
]
