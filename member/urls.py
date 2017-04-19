from django.conf.urls import url

import member
from member import views
from member.views import UserMemberUpdate

urlpatterns = [
    # url(r'^$', member.views.ListContactView.as_view(),
    # name='contacts-list', ),
    url(r'^$', views.index, name='index'),
    url(r'^mybadges/$', views.mybadges, name='mybadges'),
    url(r'^skills_matrix/$', views.skills_matrix, name='skills_matrix'),
    url(r'^skills_matrix/merit_badges/$', views.merit_badges, name='merit_badges'),
    url(r'^skills_matrix/technical/$', views.technical, name='technical'),
    url(r'^skills_matrix/social/$', views.social, name='social'),
    url(r'^skills_matrix/social/attacking/$', views.attacking, name='attacking'),
    url(r'^skills_matrix/social/leadership/$', views.leadership, name='leadership'),
    url(r'^skills_matrix/social/teamwork/$', views.teamwork, name='teamwork'),
    url(r'^skills_matrix/social/defending/$', views.defending, name='defending'),
    url(r'^skills_matrix/psychological/$', views.psychological, name='psychological'),
    url(r'^skills_matrix/psychological/kickups/$', views.kickups, name='kickups'),
    url(r'^skills_matrix/physical/$', views.physical, name='physical'),
    url(r'^add_member/$', views.add_member, name='add_member'),
    url(r'^register_profile/$', views.register_profile, name='register_profile'),
    url(r'^profile/(?P<username>[\w\-.@]+)/$', views.profile, name='profile'),
    url(r'^profile/(?P<username>[\w\-.@]+)/add_player/$', views.add_player, name='add_player'),
    url(r'^profile/(?P<username>[\w\-.@]+)/update_member/$', UserMemberUpdate.as_view(), name='usermember_update'),
]
