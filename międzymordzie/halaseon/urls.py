"""halaseon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^$', include('pomiary.urls')),
    url(r'^ajax/', include('pomiary.urls')),
    url(r'^pomiary/', include('pomiary.urls')),
    url(r'^admin/', admin.site.urls),
]

handler400 = 'pomiary.views.handler400'
handler403 = 'pomiary.views.handler403'
handler404 = 'pomiary.views.handler404'
handler500 = 'pomiary.views.handler500'
