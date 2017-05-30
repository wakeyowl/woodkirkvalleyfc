from django.conf.urls import url

from member import views
from woodkirkvalleydata import settings
from django.conf.urls.static import static

urlpatterns = [
                  # url(r'^$', member.views.ListContactView.as_view(),
                  # name='contacts-list', ),
                  url(r'^$', views.index, name='index'),
                  # url(r'^mybadges/$', views.mybadges, name='mybadges'),
                  url(r'^add_member/$', views.add_member, name='add_member'),
                  url(r'^register_profile/$', views.register_profile, name='register_profile'),
                  url(r'^profile/$', views.profile, name='profile'),
                  url(r'^accidentform/$', views.register_accident, name='register_accident'),
                  url(r'^profile/addplayer/$', views.addplayer, name='addplayer'),
                  url(r'^profile/update/$', views.update_user, name='update_user'),
                  url(r'^profile/updateplayer/$', views.update_player, name='update_player'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
