#The Model serves as the data access layer, handling 
# the structure and validation of your application data
from django.db import models

class Song(models.Model):
    #id: an automatically generated primary key.
    title = models.CharField(max_length=150, unique=True)
    artist = models.CharField(max_length=150)
    duration = models.PositiveIntegerField(help_text='Seconds')
    audio_url = models.URLField(blank=True)
    cover_url = models.URLField(blank=True)#cover image URL.

#It stores playlist information separately from song information.
class Playlist(models.Model):
    name = models.CharField(max_length=100, unique=True)

class PlaylistSong(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    position = models.PositiveIntegerField(default=0)
    class Meta:
        #constraints prevents the same song from being added to the same playlist more than once.
        constraints = [models.UniqueConstraint(fields=['playlist','song'], name='unique_playlist_song')]
        #position controls the ordering of songs within a playlist.
        ordering = ['position','id']
