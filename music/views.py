from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.response import Response
from rest_framework import status
from .models import Song
from .serializer import SongSerializer

# Create your views here.

# (5 points) As a developer, I want to create a GET by id endpoint that does the following things:
# Accepts a value from the request’s URL (The id of the song to retrieve).
# Returns a 200 status code.
# Responds with the song in the database that has the id that was sent through the URL.

# (5 points) As a developer, I want to create a POST endpoint that does the following things:
# Accepts a body object from the request in the form of a Song model.
# Adds the new song to the database.
# Returns a 201 status code.
# Responds with the newly created song object.

@api_view (['GET', 'POST'])
def song_list(request):
    if request.method == 'GET': #200 OK
        song = Song.objects.all()
    elif request.method == 'POST': #201 Created
        serializer = SongSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    serializer = SongSerializer(song, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

def song_like(request, pk):
    song = get_object_or_404(Song, id=request.POST.get('song id'))
    if song.likes.filter(id=request.user.id).exists():
        song.likes.remove(request.user)
    else:
        song.likes.add(request.user)

    return HttpResponseRedirect(reverse('song detail', args=[str(pk)]))

class SongDetailView(DetailView):
    model = Song

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        likes_connected = get_object_or_404(Song, id=self.kwargs['pk'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['number of likes'] = likes_connected.number_of_likes()
        data['song is liked'] = liked
        return data



# (5 points) As a developer, I want to create a PUT endpoint that does the following things:
# Accepts a value from the request’s URL (The id of the song to be updated).
# Accepts a body object from the request in the form of a Song model.
# Finds the song in the Music table and updates that song with the properties that were sent in the request’s body.
# Returns a 200 status code.
# Responds with the newly updated song object.

# (5 points) As a developer, I want to create a DELETE endpoint that does the following things:
# Accepts a value from the request’s URL. (The id of the song to delete).
# Returns a 204 status code.

@api_view (['GET', 'PUT', 'DELETE']) 
def song_detail(request, pk):
    song = get_object_or_404(Song, pk=pk)
    if request.method == 'GET': #200 OK
        serializer = SongSerializer(song);
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT': #specific product ID, #200 OK
        serializer = SongSerializer(song, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save();
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE': #204 code
        song.delete();
        return Response(status=status.HTTP_204_NO_CONTENT)


# (5 points) As a developer, I want to use Postman to make a POST, PUT, DELETE, and both GET requests (get by id and get all) 
# request to my REST web API, save it to a collection, and then export it as a JSON from Postman.

# BONUS
# (5 points) As a developer, I want to add the ability to “like” a song through the web API and 
# have the number of likes saved in the database with the song.



