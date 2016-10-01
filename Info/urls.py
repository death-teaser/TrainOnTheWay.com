from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^index/$', views.index, name='index'),
    url(r'^index2/$', views.getavailability, name='getavailability'),
    url(r'^developer/$', views.developer, name='developer'),
]
