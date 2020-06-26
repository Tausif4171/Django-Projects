from django.conf.urls import url
from . import views

app_name = 'music'

urlpatterns = [
    #/music/
    url(r'^$',views.IndexView,name='index'),

    #/music/register/
    url(r'^register/$',views.UserFormView.as_view(),name='register'),

    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),

    #/music/<album_id>/
    url(r'^(?P<album_id>[0-9]+)/$',views.DetailView,name='detail'), 

     # /music/album/add/ 
     url(r'album/add/$',views.AlbumCreate,name='album-add'), #for creating new album 

    # /music/album/2/ 
     url(r'album/(?P<pk>[0-9]+)/$',views.AlbumUpdate.as_view(),name='album-update'), #for album editing

     
    # /music/album/2/delete 
     url(r'album/(?P<pk>[0-9]+)/delete/$',views.AlbumDelete.as_view(),name='album-delete'), #for album deleting

    # /music/5/create_song/
    url(r'^(?P<album_id>[0-9]+)/create_song/$', views.create_song, name='create_song'),

    # 
    url(r'^(?P<song_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),

    url(r'^(?P<album_id>[0-9]+)/favorite_album/$', views.favorite_album, name='favorite_album'),

    # /music/5/delete_song/1/
    url(r'^(?P<album_id>[0-9]+)/delete_song/(?P<song_id>[0-9]+)/$', views.delete_song, name='delete_song'),

    # /music/songs/all/
    url(r'^songs/(?P<filter_by>[a-zA_Z]+)/$', views.songs, name='songs'),


]