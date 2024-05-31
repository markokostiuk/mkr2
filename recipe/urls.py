from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('category_detail/<int:id>/', views.category_detail, name='category_detail'),
]
