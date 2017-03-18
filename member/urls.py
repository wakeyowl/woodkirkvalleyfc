from django.conf.urls import url

import member
from member import views
from member.views import UserMemberUpdate

urlpatterns = [
    # url(r'^$', member.views.ListContactView.as_view(),
    # name='contacts-list', ),
    url(r'^$', views.index, name='index'),
    url(r'^skills_matrix/$', views.skills_matrix, name='skills_matrix'),
    url(r'^skills_matrix/technical$', views.technical, name='technical'),
    url(r'^add_member/$', views.add_member, name='add_member'),
    url(r'^register_profile/$', views.register_profile, name='register_profile'),
    url(r'^profile/(?P<username>[\w\-.@]+)/$', views.profile, name='profile'),
    url(r'^profile/(?P<username>[\w\-.@]+)/add_player/$', views.add_player, name='add_player'),
    url(r'^profile/(?P<username>[\w\-.@]+)/update_member/$', UserMemberUpdate.as_view(), name='usermember_update'),
]
