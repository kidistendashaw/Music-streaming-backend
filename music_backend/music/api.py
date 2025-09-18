from ninja import NinjaAPI
from .models import Song, Playlist, FavoriteSong
from ninja import Schema
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

api = NinjaAPI()

class SongSchema(Schema):
    id: int
    title: str
    artist: str
    album: str
    audio_file: str
    cover_image: str | None

@api.get("/songs")
def list_songs(request):
    songs = Song.objects.all()
    return [SongSchema(
        id=s.id,
        title=s.title,
        artist=s.artist,
        album=s.album,
        audio_file=s.audio_file.url,
        cover_image=s.cover_image.url if s.cover_image else None
    ) for s in songs]

@api.get("/search")
def search_songs(request, q: str):
    songs = Song.objects.filter(title__icontains=q) | Song.objects.filter(artist__icontains=q)
    return [{"id": s.id, "title": s.title, "artist": s.artist, "album": s.album, "audio_file": s.audio_file.url} for s in songs]

@api.post("/favorites")
def add_favorite(request, song_id: int):
    user = request.user
    song = get_object_or_404(Song, id=song_id)
    FavoriteSong.objects.get_or_create(user=user, song=song)
    return {"message": "Added to favorites"}

@api.get("/favorites")
def list_favorites(request):
    user = request.user
    favs = FavoriteSong.objects.filter(user=user)
    return [{"id": f.song.id, "title": f.song.title} for f in favs]
