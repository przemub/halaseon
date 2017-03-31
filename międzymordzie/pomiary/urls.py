from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^live_update/$', views.live_update, name="live_update"),
]
