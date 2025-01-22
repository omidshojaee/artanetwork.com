"""
URL configuration for products app.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path(
        '<slug:category_slug>/',
        views.SubcategoryListView.as_view(),
        name='subcategory_list',
    ),
    path(
        '<slug:category_slug>/<slug:subcategory_slug>/',
        views.ProductListView.as_view(),
        name='product_list',
    ),
    path(
        '<slug:category_slug>/<slug:subcategory_slug>/<slug:product_slug>/',
        views.ProductDetailView.as_view(),
        name='product_detail',
    ),
]
