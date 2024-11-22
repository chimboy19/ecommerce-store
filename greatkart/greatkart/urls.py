"""
URL configuration for greatkart project.

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
from django.contrib import admin
from django.urls import include, path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.utils.translation import gettext_lazy as _
# install django-admin-honeyport to create fake admin panel record hacking attempts
urlpatterns = [
   # path('admin/',include('admin_honeypot.urls',namespace='admin_honeypot')),
    path('vibeadmin/', admin.site.urls),
    path('', views.Home,name='home'),
    path('store/', include('store.urls')),
    path('cart/', include('carts.urls')),
    path('accounts/', include('accounts.urls')),
    path('orders/', include('orders.urls')),

] #+ static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)
if not settings.DEBUG:  # Only serve media files in production
    from django.views.static import serve
    from django.urls import re_path

    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]