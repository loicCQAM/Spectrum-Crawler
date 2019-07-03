import sys
import lastFM
import spotifyAPI
import json
import database

def populate_database(max_genres, songs_per_genre):
    database.connect()
    print("***** SPECTRUM CRAWLER *****")
    print("")

    print("Step 1 --- lastFM extraction")

    lastFM_songs = []
    songs = []
    numSongs = 0

    # get genres
    genres = lastFM.get_genres(max_genres)
    genresMap = {}

    print(str(len(genres)) + " genres retrieved")

    # get songs
    for genre in genres:
        # add to database
        genre_id = database.insert_genre(genre)
        if (genre_id is not False):
            genresMap[genre] = genre_id 

        # extraction
        extraction = lastFM.get_songs_per_genre(genre, [], 1, songs_per_genre)
        lastFM_songs = lastFM_songs + extraction

    print(str(len(lastFM_songs)) + " songs retrieved")

    print("")
    print("Step 2 --- Spotify extraction")
    for song in lastFM_songs:
        s = spotifyAPI.search_song(song['title'], song['artist'])
        if (s is not False):
            s['genre'] = song['genre']
            if s['genre'] in genresMap:
                id_song = database.insert_song(s['title'], s['artist'], genresMap[s['genre']])
                if (id_song is not False) :
                    numSongs = numSongs + 1
                    # TODO : insérer les primitives
                    '''for primitive, value in s['primitives'].items():
                        #database.insert_song_primitive(id_song, primitive, value)'''

    print(str(numSongs) + " songs added")
    if (numSongs < len(lastFM_songs)):
        print(str(len(lastFM_songs) - numSongs) + " songs lost in conversion")

    with open('songs.json', 'w') as outfile:
        json.dump(songs, outfile)

    database.disconnect()
    print("")
    print("DONE !")
    print("")

if (len(sys.argv) < 3):
    sys.exit("Missing parameters")
elif (not sys.argv[1].isdigit() or not sys.argv[2].isdigit()):
    sys.exit("Bad parameter type")
else:
    populate_database(int(sys.argv[1]), int(sys.argv[2]))
