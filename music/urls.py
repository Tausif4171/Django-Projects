from django.conf.urls import url
from . import views

app_name = 'music'

urlpatterns = [
    #/music/
    url(r'^$',views.IndexView.as_view(),name='index'),

    #/music/register/
    url(r'^register/$',views.UserFormView.as_view(),name='register'),

    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),

    #/music/<album_id>/
    url(r'^(?P<pk>[0-9]+)/$',views.DetailView.as_view(),name='detail'), #here we are writing as_view() function,
                                                                        # because we are converting our class into view function
     # /music/album/add/ 
     url(r'album/add/$',views.AlbumCreate.as_view(),name='album-add'), #for creating new album 

    # /music/album/2/ 
     url(r'album/(?P<pk>[0-9]+)/$',views.AlbumUpdate.as_view(),name='album-update'), #for album editing

     
    # /music/album/2/delete 
     url(r'album/(?P<pk>[0-9]+)/delete/$',views.AlbumDelete.as_view(),name='album-delete'), #for album deleting
]