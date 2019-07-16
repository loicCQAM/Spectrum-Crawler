import sys
import requests
import database

api_key = "496a61caa0ce335911b9cbea2d15e1c9"
base_url = "http://ws.audioscrobbler.com/2.0/"
signature = "&api_key=" + api_key + "&format=json"


def get_genres(max_genres, offset):
    genres = []

    # construct query
    query = "?method=tag.getTopTags&offset=" + str(offset) + "&num_res=" + str(max_genres)

    # call API
    request = requests.get(base_url + query + signature)

    # manage response
    if (request.status_code != 200):
        sys.exit("Error: Code " + str(request.status_code))
    else:
        if (request.json()['toptags']['tag']):
            for genre in request.json()['toptags']['tag']:
                genres.append(genre['name'])
    return genres


def get_songs_per_genre(genre, genre_id, songs, page, songs_per_genre):
    # construct query
    query = "?method=tag.gettoptracks&tag=" + genre + "&page=" + str(page)

    # call API
    request = requests.get(base_url + query + signature)

    # manage response
    if (request.status_code != 200):
        sys.exit("Error: Code " + str(request.status_code))
    else:
        if (request.json()['tracks']['track']):
            # attributes
            attributes = request.json()['tracks']['@attr']
            currentPage = attributes['page']
            isLastPage = currentPage == attributes['totalPages']

            # loop songs
            for track in request.json()['tracks']['track']:
                if (len(songs) < int(songs_per_genre) and not database.song_exists(track['name'], track['artist']['name'])):
                    song = {}
                    song['title'] = track['name']
                    song['artist'] = track['artist']['name']
                    song['genre'] = genre
                    songs.append(song)

                    # add song to dtabase
                    database.insert_song(song['title'], song['artist'], genre_id)

            # recursive part of the algorithm
            if (len(songs) < int(songs_per_genre) and not isLastPage):
                nextPage = int(currentPage) + 1
                return get_songs_per_genre(genre, genre_id, songs, nextPage, songs_per_genre)
            else:
                return songs
