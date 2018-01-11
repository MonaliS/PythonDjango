from django.shortcuts import render, get_object_or_404
from .models import Album,Song
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserForm
from django.views.generic import View

#from django.http import Http404


#def index(request):
    #all_albums = Album.objects.all()
   # template = loader.get_template('music/index.html')
   # context = {
   #     'all_albums': all_albums
    #}
    #return HttpResponse(template.render(context),request)


#def detail(request,album_id):
  #  album = get_object_or_404(Album,pk=album_id)
   # template = loader.get_template('music/detail.html')
   # context = {
   #     'album': album
   # }
   # return HttpResponse(template.render(context),request)


def favourite(request,album_id):
    album = get_object_or_404(Album,pk=album_id)
    try:
        selected_song=album.song_set.get(pk=request.POST["song"])
    except (KeyError, Song.DoesNotExist):
        template = loader.get_template('music/detail.html')
        context = {
            'album': album,
            'error_message':'you did not select valid song'
        }
        return HttpResponse(template.render(context), request)
    else:
        selected_song.is_favourite=True
        selected_song.save()
        template = loader.get_template('music/detail.html')
        context = {
            'album': album,
        }
        return HttpResponse(template.render(context), request)


class IndexView(generic.ListView):
    template_name = 'music/index.html'
    context_object_name = 'all_albums'

    def get_queryset(self):
        return Album.objects.all();


class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'


class AlbumCreate(CreateView):
    model = Album
    fields = ['artist','album_title','genre','album_logo']


class AlbumUpdate(UpdateView):
    model = Album
    fields = ['artist','album_title','genre','album_logo']


class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('index')


class UserFormView(View):
    form_class = UserForm
    template_name = 'music/registration_form.html'

    #display blank form
    def get(self,request):
        form=self.form_class(None)
        return render(request,self.template_name,{'form':form})

    #display form data
    def post(self,request):
        form =self.form_class(request.POST)

        if form.is_valid():
            user=form.save(commit=False)

            #cleaned data
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user.set_password(password)

            user.save()

            #returns user object if credentials are correct
            user = authenticate(username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('index')

        return render(request,self.template_name,{'form':form})





