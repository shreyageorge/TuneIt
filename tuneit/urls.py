#Django URL routing is the connection between the browser 
# and the Python functions that implement your features.
from django.urls import path
from music import views
urlpatterns = [
    path('', views.home),
    path('api/songs/', views.songs), #retrieves all songs as JSON
    path('api/search/', views.search),
    path('api/sort/', views.sort_songs),#sort by duration
    path('api/song/add/', views.add_song),
    path('api/song/delete/', views.delete_song),
    path('api/playlists/', views.playlists),
    path('api/playlist/add/', views.add_to_playlist),
    path('api/playlist/remove/', views.remove_from_playlist),
]
