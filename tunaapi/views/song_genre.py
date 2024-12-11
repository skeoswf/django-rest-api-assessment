from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import SongGenre, Song, Genre


class SongGenreView(ViewSet):

    def retrieve(self, request, pk):
        song_genre = SongGenre.objects.get(pk=pk)
        serializer = SongGenreSerializer(song_genre)
        return Response(serializer.data)

    def list(self, request):
        song_genres = SongGenre.objects.all()
        serializer = SongGenreSerializer(song_genres, many=True)
        return Response(serializer.data)

    def create(self, request):

        song = Song.objects.get(pk=request.data["SongId"])
        genre = Genre.objects.get(pk=request.data["GenreId"])

        song_genre = SongGenre.objects.create(
            song=song,
            genre=genre
        )

        serializer = SongGenreSerializer(song_genre)
        return Response(serializer.data)

    def update(self, request, pk):

        song_genre = SongGenre.objects.get(pk=pk)

        song_genre.song = Song.objects.get(pk=request.data["SongId"])
        song_genre.genre = Genre.objects.get(pk=request.data["GenreId"])

        song_genre.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):

        song_genre = SongGenre.objects.get(pk=pk)
        song_genre.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class SongGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongGenre
        fields = (
            'id',
            'song_id',
            'genre_id',
        )
