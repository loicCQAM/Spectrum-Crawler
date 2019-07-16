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

    # basic song info from API
    result = sp.search(q=title + ', ' + artist, type='track', limit=1)
    if (result['tracks']['items'] and len(result['tracks']['items']) > 0):
        s = result['tracks']['items'][0]
        song['spotify_id'] = s['id']
        song['title'] = title
        song['artist'] = artist
        song['album'] = s['album']['name']
        song['art'] = s['album']['images'][0]['url']
        song['sound'] = s['preview_url']
        song['artist'] = artist
        song['primitives'] = {}

        # get primitives from API
        features = sp.audio_features([song['spotify_id']])
        if (features and features[0] is not None):
            song['primitives']['duration'] = features[0]['duration_ms']
            song['primitives']['energy'] = features[0]['energy']
            song['primitives']['liveness'] = features[0]['liveness']
            song['primitives']['tempo'] = features[0]['tempo']
            song['primitives']['speechiness'] = features[0]['speechiness']
            song['primitives']['acousticness'] = features[0]['acousticness']
            song['primitives']['instrumentalness'] = features[0]['instrumentalness']
            song['primitives']['time_signature'] = features[0]['time_signature']
            song['primitives']['danceability'] = features[0]['danceability']
            song['primitives']['key'] = features[0]['key']
            song['primitives']['loudness'] = features[0]['loudness']
            song['primitives']['valence'] = features[0]['valence']
        else:
            return False
    else:
        return False

    return song
