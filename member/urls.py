from django.conf.urls import url
from member import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]