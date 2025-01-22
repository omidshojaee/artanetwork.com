"""
URL configuration for homepage app.

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

app_name = 'homepage'

urlpatterns = [
    path('', views.HomepageView.as_view(), name='index'),
    path('contact/', views.ContactView.as_view(), name='contact_view'),
    path(
        'newsletter/signup/',
        views.NewsletterView.as_view(),
        name='newsletter_signup_view',
    ),
]
