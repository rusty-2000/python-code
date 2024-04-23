from django.urls import path, re_path
from . import views
from rest_framework import permissions

urlpatterns = [

    path('', views.ProductList.as_view(), name='product-list'),
    path('<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),
    path('<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),
]