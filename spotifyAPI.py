import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# credentials
client_id = "3c4a4638369448f0b4e3aa384a1d3d23"
client_secret = "6806c20823fd4d718ea8f3e0354caf8a"

# login to Spotify
client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def search_song(title, artist):
    song = {}
    result = sp.search(q=title + ', ' + artist, type='track', limit=1)
    if (result['tracks']['items'] and len(result['tracks']['items']) > 0):
        s = result['tracks']['items'][0]
        song['id'] = s['id']
        song['title'] = title
        song['artist'] = artist
        song['primitives'] = {}
        song['primitives']['popularity'] = s['popularity']
        song['primitives']['duration'] = s['duration_ms']
    else:
        return False

    return song


def get_song(title, artist):
    song = search_song(title, artist)
    return song
