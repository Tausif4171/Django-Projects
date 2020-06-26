from django.contrib.auth import authenticate, login #this one is for your authenticate of your username and password that present in your database or not just verify... and login provides session-id so that user do not want to login or authenticate for every pages in browser that you are..
from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView # means here we are importing methods for album
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect #this one redirect you to your home page and whatever you are
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic import View
from .models import Album, Song
from .forms import AlbumForm, SongForm, UserForm
from django.db.models import Q

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

def IndexView(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        all_albums = Album.objects.filter(user=request.user)
        song_results = Song.objects.all()
        query = request.GET.get("q")
        if query:
            all_albums = all_albums.filter(
                Q(album_title__icontains=query) |
                Q(artist__icontains=query)
            ).distinct()
            song_results = song_results.filter(
                Q(song_title__icontains=query)
            ).distinct()
            return render(request, 'music/index.html', {
                'all_albums': all_albums,
                'songs': song_results,
            })
        else:
            return render(request, 'music/index.html', {'all_albums': all_albums})

def DetailView(request, album_id):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        user = request.user
        album = get_object_or_404(Album, pk=album_id)
        return render(request, 'music/detail.html', {'album': album, 'user': user})


def AlbumCreate(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        form = AlbumForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user
            album.album_logo = request.FILES['album_logo']
            file_type = album.album_logo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'music/album_form.html', context)
            album.save()
            return render(request, 'music/detail.html', {'album': album})
        context = {
            "form": form,
        }
        return render(request, 'music/album_form.html', context)


class AlbumUpdate(UpdateView):
    #here we are creating new album_object
    model= Album
    fields = ['artist', 'album_title', 'genre', 'album_logo'] #here we are creating fields that user has to be filledup

class AlbumDelete(DeleteView):
    #here we are creating new album_object
    model= Album
    success_url = reverse_lazy('music:index') #when you deleted album it redirect to home page by using reverse_lazy function

def create_song(request, album_id):
    form = SongForm(request.POST or None, request.FILES or None)
    album = get_object_or_404(Album, pk=album_id)
    if form.is_valid():
        albums_songs = album.song_set.all()
        for s in albums_songs:
            if s.song_title == form.cleaned_data.get("song_title"):
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'You already added that song',
                }
                return render(request, 'music/create_song.html', context)
        song = form.save(commit=False)
        song.album = album
        song.audio_file = request.FILES['audio_file']
        file_type = song.audio_file.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in AUDIO_FILE_TYPES:
            context = {
                'album': album,
                'form': form,
                'error_message': 'Audio file must be WAV, MP4, or OGG',
            }
            return render(request, 'music/create_song.html', context)

        song.save()
        return render(request, 'music/detail.html', {'album': album})
    context = {
        'album': album,
        'form': form,
    }
    return render(request, 'music/create_song.html', context)


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'music/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'albums': albums})
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid login'})
    return render(request, 'music/login.html')      


class UserFormView(View):
    form_class = UserForm # Here, from forms.py file we are accessing UserForm class 
    template_name = 'music/registration_form.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None) # here 'form' is an object
        return render(request, self.template_name, {'form': form})    

    # process form data
    def post(self,request):
        form = self.form_class(request.POST)
 
        if form.is_valid():

            user = form.save(commit=False) 
 
            # cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password) # Using set_password function the user changed his password
            user.save() # this line saves the user to the database

            # returns User objects if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active: # here it checks in datatabase the user is active or banned 
                    login(request, user) # Now user is login to our website
                    return redirect('music:index') # if user is login successfully it will be redirect to index or home page

        return render(request, self.template_name, {'form': form}) # if form is not valid than this will be return 

def favorite(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    try:
        if song.is_favorite:
            song.is_favorite = False
        else:
            song.is_favorite = True
        song.save()
    except (KeyError, Song.DoesNotExist):
        return JsonResponse({'success': False})
    finally:
        return JsonResponse({'success': True})

def favorite_album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    try:
        if album.is_favorite:
            album.is_favorite = False
        else:
            album.is_favorite = True
        album.save()
    except (KeyError, Album.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def delete_song(request, album_id, song_id):
    album = get_object_or_404(Album, pk=album_id)
    song = Song.objects.get(pk=song_id)
    song.delete()
    return render(request, 'music/detail.html', {'album': album})
    

def songs(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        try:
            song_ids = []
            for album in Album.objects.filter(user=request.user):
                for song in album.song_set.all():
                    song_ids.append(song.pk)
            users_songs = Song.objects.filter(pk__in=song_ids)
            if filter_by == 'favorites':
                users_songs = users_songs.filter(is_favorite=True)
        except Album.DoesNotExist:
            users_songs = []
        return render(request, 'music/songs.html', {
            'song_list': users_songs,
            'filter_by': filter_by,
        })
