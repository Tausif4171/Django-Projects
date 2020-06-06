from django.views.generic.edit import CreateView, UpdateView, DeleteView # means here we are importing methods for album
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect #this one redirect you to your home page and whatever you are
from django.contrib.auth import authenticate, login #this one is for your authenticate of your username and password that present in your database or not just verify... and login provides session-id so that user do not want to login or authenticate for every pages in browser that you are..
from django.views import generic
from django.views.generic import View
from .models import Album
from .forms import UserForm

class IndexView(generic.ListView):
    template_name= 'music/index.html'
    context_object_name = 'all_albums' #you can give anyname and then give that same as to index.html

    #this is query for getting objects from database
    def get_queryset(self):
        return Album.objects.all() #getting all objects from database

class DetailView(generic.DetailView):
    model= Album #this is for getting detail of Album objects
    template_name= 'music/detail.html'

#here we are creating a class for creating  a new album and inheriting from CreateView
class AlbumCreate(CreateView):
    #here we are creating new album_object
    model= Album
    fields = ['artist', 'album_title', 'genre', 'album_logo'] #here we are creating fields that user has to be filledup

class AlbumUpdate(UpdateView):
    #here we are creating new album_object
    model= Album
    fields = ['artist', 'album_title', 'genre', 'album_logo'] #here we are creating fields that user has to be filledup

class AlbumDelete(DeleteView):
    #here we are creating new album_object
    model= Album
    success_url = reverse_lazy('music:index') #when you deleted album it redirect to home page by using reverse_lazy function

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



    