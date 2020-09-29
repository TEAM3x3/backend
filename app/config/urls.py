"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin

from django.urls import path, include

from core.views import index, success, fail
from .yasg import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('payment/', index, name='index'),
    path('success/', success),
    path('fail', fail)
]

urlpatterns += static('settings.base.MEDIA_URL', document_root='settings.base.MEDIA_ROOT')
urlpatterns += urlpatterns_yasg
