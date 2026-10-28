#This file imports Django utilities, your database models and your DSA implementations:

#reads JSON sent by the browser.
import json
#returns data to JavaScript.
from django.http import JsonResponse
#renders your HTML template.
from django.shortcuts import render
#restricts a function to POST requests.
from django.views.decorators.http import require_POST
from .models import Song, Playlist, PlaylistSong
from .dsa import BST, merge_sort, binary_search_duration

#This fetches the song records from the database 
#and converts them into a Python list of dictionaries.
def song_data(song_id):
    return Song.objects.values(
        'id', 'title', 'artist', 
        'duration', 'audio_url', 'cover_url'
    ).get(pk=song_id)

def title_for_id(song_id):
    return Song.objects.values_list('title', flat=True).get(pk=song_id)

def duration_for_id(song_id):
    return Song.objects.values_list('duration', flat=True).get(pk=song_id)

#This function creates a new BST and inserts each song dictionary into it.
def tree():
    bst = BST(title_for_id)
    for song_id in Song.objects.values_list('id', flat=True).iterator():
        bst.insert(song_id)
    return bst

def home(request):
    return render(request, 'index.html')

def songs(request):
    return JsonResponse({'songs': [song_data(song_id) for song_id in tree().inorder()]})

def search(request):
    method = request.GET.get('method', 'bst')
    if method == 'bst':
        song_id, count = tree().search(request.GET.get('q','').strip())
        matches = [song_data(song_id)] if song_id is not None else []
        return JsonResponse({'songs': matches, 'comparisons':count, 'algorithm':'BST title search'})
    try:
        seconds = int(request.GET.get('q',''))
    except ValueError:
        return JsonResponse({'error':'Enter duration in seconds'}, status=400)
    song_ids = list(Song.objects.values_list('id', flat=True))
    sorted_ids, _ = merge_sort(song_ids, duration_for_id)
    matches, count = binary_search_duration(sorted_ids, seconds, duration_for_id)
    return JsonResponse({
        'songs': [song_data(song_id) for song_id in matches],
        'comparisons':count,
        'algorithm':'Binary search by duration',
    })

def sort_songs(request):
    song_ids = list(Song.objects.values_list('id', flat=True))
    sorted_ids, count = merge_sort(song_ids, duration_for_id)
    return JsonResponse({
        'songs': [song_data(song_id) for song_id in sorted_ids],
        'comparisons':count,
        'algorithm':'Merge sort by duration',
    })

def payload(request):
    try:
        return json.loads(request.body or '{}')
    except (ValueError, UnicodeDecodeError):
        return {}

@require_POST
def add_song(request):
    p = payload(request)
    try:
        title = str(p.get('title','')).strip()
        artist = str(p.get('artist','')).strip()
        duration = int(p.get('duration',0))
        if not title or not artist or duration <= 0:
            raise ValueError('Title, artist and positive duration required')
        if tree().search(title)[0] is not None:
            raise ValueError('Title already exists in BST')
        song = Song.objects.create(title=title,artist=artist,duration=duration,
                                   audio_url=p.get('audio_url',''),cover_url=p.get('cover_url',''))
        return JsonResponse({'ok':True,'id':song.id})
    except (ValueError, TypeError) as exc:
        return JsonResponse({'error':str(exc)}, status=400)

@require_POST
def delete_song(request):
    p = payload(request)
    title = str(p.get('title','')).strip()
    bst = tree()
    song_id, count = bst.search(title)
    if song_id is None:
        return JsonResponse({'error':'Song not found','comparisons':count}, status=404)
    bst.delete(title)
    Song.objects.filter(pk=song_id).delete()
    return JsonResponse({'ok':True,'comparisons':count})

def playlists(request):
    if request.method == 'POST':
        name = str(payload(request).get('name','')).strip()
        if not name:
            return JsonResponse({'error':'Playlist name required'},status=400)
        playlist, created = Playlist.objects.get_or_create(name=name)
        return JsonResponse({'ok':True,'id':playlist.id,'created':created})
    result = []
    for p in Playlist.objects.all().order_by('id'):
        result.append({'id':p.id,'name':p.name,'song_ids':list(p.playlistsong_set.values_list('song_id',flat=True))})
    return JsonResponse({'playlists':result})

@require_POST
def add_to_playlist(request):
    p = payload(request)
    try:
        playlist = Playlist.objects.get(pk=p.get('playlist_id'))
        song = Song.objects.get(pk=p.get('song_id'))
    except (Playlist.DoesNotExist, Song.DoesNotExist, ValueError, TypeError):
        return JsonResponse({'error':'Playlist or song not found'},status=404)
    last = PlaylistSong.objects.filter(playlist=playlist).order_by('-position').first()
    PlaylistSong.objects.get_or_create(playlist=playlist,song=song,defaults={'position':last.position+1 if last else 0})
    return JsonResponse({'ok':True})

@require_POST
def remove_from_playlist(request):
    p = payload(request)
    PlaylistSong.objects.filter(playlist_id=p.get('playlist_id'),song_id=p.get('song_id')).delete()
    return JsonResponse({'ok':True})
