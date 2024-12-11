from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Artist, Song


class ArtistView(ViewSet):

    def retrieve(self, request, pk):
        artist = Artist.objects.get(pk=pk)
        songs = Song.objects.filter(artist=artist)
        song_serializer = SongSerializer(songs, many=True)
        artist_data = ArtistSerializer(artist).data
        artist_data['song_count'] = songs.count()
        artist_data['songs'] = song_serializer.data
        return Response(artist_data)

    def list(self, request):
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)

    def create(self, request):
        artist = Artist.objects.create(
            name=request.data["name"],
            age=request.data["age"],
            bio=request.data["bio"],
        )

        serializer = ArtistSerializer(artist)
        return Response(serializer.data)

    def update(self, request, pk):

        artist = Artist.objects.get(pk=pk)

        artist.name = request.data["name"]
        artist.age = request.data["age"]
        artist.bio = request.data["bio"]

        artist.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):

        artist = Artist.objects.get(pk=pk)
        artist.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class SongSerializer(serializers.ModelSerializer):

    class Meta:
        model = Song
        fields = (
            'id',
            'title',
            'artist_id',
            'album',
            'length',
        )


class ArtistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = (
            'id',
            'name',
            'age',
            'bio'
        )


class SingleArtistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = (
            'id',
            'name',
            'age',
            'bio',
            'song_count',
            'songs'
        )
