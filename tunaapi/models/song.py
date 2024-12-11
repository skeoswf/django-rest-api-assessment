from django.db import models
from .artist import Artist
from .genre import Genre


class Song(models.Model):
    title = models.CharField(max_length=25)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    album = models.CharField(max_length=25)
    length = models.PositiveIntegerField()
