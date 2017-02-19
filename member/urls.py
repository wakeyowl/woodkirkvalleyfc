from django.conf.urls import url
from member import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_member/$', views.add_member, name='add_member'),
    url(r'^register_profile/$', views.register_profile, name='register_profile'),
    url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
]
