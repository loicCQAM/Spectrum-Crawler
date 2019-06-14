import sys
import lastFM
import spotifyAPI

print("***** SPECTRUM CRAWLER *****")
print("")

if (len(sys.argv) < 3):
    sys.exit("Missing parameters")
elif (not sys.argv[1].isdigit() or not sys.argv[2].isdigit()):
    sys.exit("Bad parameter type")
else:
    print("Step 1 --- lastFM extraction")

    songs = []
    max_genres = int(sys.argv[1])
    songs_per_genre = int(sys.argv[2])

    # get genres
    genres = lastFM.get_genres(max_genres)

    print(str(len(genres)) + " genres retrieved")

    # get songs
    for genre in genres:
        extraction = lastFM.get_songs_per_genre(genre, [], 1, songs_per_genre)
        songs = songs + extraction

    print(str(len(songs)) + " songs retrieved")

    print("")
    print("Step 2 --- Spotify extraction")
    for song in songs:
        s = spotifyAPI.search_song(song['title'], song['artist'])
        print(s)

    print("")
    print("DONE !")
    print("")
