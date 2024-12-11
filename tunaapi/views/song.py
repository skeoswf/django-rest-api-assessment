from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Song, Artist, Genre


class SongView(ViewSet):

    def retrieve(self, request, pk):
        song = Song.objects.get(pk=pk)
        genres = Genre.objects.filter(songgenre__song_id=song)
        song.genres = genres.all()
        serializer = SongSingleSerializer(song)
        return Response(serializer.data)

    def list(self, request):
        songs = Song.objects.all()
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)

    def create(self, request):

        artist = Artist.objects.get(pk=request.data["artistId"])

        song = Song.objects.create(
            title=request.data["title"],
            artist=artist,
            album=request.data["album"],
            length=request.data["length"]
        )

        serializer = SongSerializer(song)
        return Response(serializer.data)

    def update(self, request, pk):

        song = Song.objects.get(pk=pk)

        song.title = request.data["title"]
        song.album = request.data["album"]
        song.length = request.data["length"]

        artist = Artist.objects.get(pk=request.data["artistId"])

        song.artist = artist

        song.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):

        song = Song.objects.get(pk=pk)
        song.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = (
            'id',
            'name',
            'age',
            'bio'
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            'id',
            'description',
        )


class SongSingleSerializer(serializers.ModelSerializer):

    artist = ArtistSerializer()
    genres = GenreSerializer(many=True)

    class Meta:
        model = Song
        fields = (
            'id',
            'title',
            'artist',
            'album',
            'length',
            'genres'
        )


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
