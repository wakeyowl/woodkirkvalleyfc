from django.conf.urls import url
from member import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_member/$', views.add_member, name='add_member'),
]
