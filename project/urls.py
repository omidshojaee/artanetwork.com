"""
URL configuration for project project.

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from filebrowser.sites import site

from accounts.forms import AuthenticationForm
from accounts.views import PasswordChangeView

admin.site.login_form = AuthenticationForm
admin.site.site_header = 'آرتا شبکه صنعت رایان'
admin.site.site_title = 'سایت آرتا شبکه صنعت رایان'
admin.site.index_title = 'پنل مدیریت'

urlpatterns = [
    path('admin/filebrowser/', site.urls),
    path('admin/password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('products/', include('products.urls', namespace='products')),
    path('', include('homepage.urls', namespace='homepage')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

