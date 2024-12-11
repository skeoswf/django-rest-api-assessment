from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Genre, Song, SongGenre


class GenreView(ViewSet):

    def retrieve(self, request, pk):
        genre = Genre.objects.get(pk=pk)

        song_genres = SongGenre.objects.filter(genre_id=genre.id)
        song_ids = [song_genre.song_id for song_genre in song_genres]
        songs = Song.objects.filter(id__in=song_ids)

        song_serializer = SongSerializer(songs, many=True)

        genre_data = GenreSerializer(genre).data

        genre_data['songs'] = song_serializer.data
        return Response(genre_data)

    def list(self, request):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)

    def create(self, request):
        genre = Genre.objects.create(
            description=request.data["description"],
        )

        serializer = GenreSerializer(genre)
        return Response(serializer.data)

    def update(self, request, pk):

        genre = Genre.objects.get(pk=pk)
        genre.description = request.data["description"]
        genre.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):

        genre = Genre.objects.get(pk=pk)
        genre.delete()
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


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            'id',
            'description',
        )


class SingleGenreSerializer(serializers.ModelSerializer):
    class Meta:
        Model = Genre
        fields = (
            'id',
            'descriptions',
            'songs'
        )
