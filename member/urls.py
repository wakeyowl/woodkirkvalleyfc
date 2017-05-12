from django.conf.urls import url

import member
from member import views

urlpatterns = [
    # url(r'^$', member.views.ListContactView.as_view(),
    # name='contacts-list', ),
    url(r'^$', views.index, name='index'),
    # url(r'^mybadges/$', views.mybadges, name='mybadges'),
    url(r'^add_member/$', views.add_member, name='add_member'),
    url(r'^register_profile/$', views.register_profile, name='register_profile'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/addplayer/$', views.addplayer, name='addplayer'),
    url(r'^profile/update/$', views.update_user, name='update_user'),

    # url(r'^profile/(?P<username>[\w\-.@]+)/update_member/$', UserMemberUpdate.as_view(), name='usermember_update'),
]
