import psycopg2
import lastFM
import spotifyAPI
from config import config

sql_insert_song = """ INSERT INTO songs(title, artist, genre_id, album_id) VALUES(%s,%s,%s, 0) RETURNING id; """
sql_select_song = """ SELECT id FROM songs WHERE title = %s AND artist = %s;"""
sql_exist_song = """ SELECT COUNT(id) FROM songs WHERE title = %s AND artist = %s;"""

sql_insert_genre = """ INSERT INTO genres(name, is_selected) VALUES(%s, true) RETURNING id;"""
sql_select_genre = """ SELECT id FROM genres WHERE name = %s;"""
sql_count_genre = """ SELECT COUNT(id) FROM genres;"""

sql_insert_primitive = """ INSERT INTO primitives(name, is_selected) VALUES(%s, true) RETURNING id; """
sql_select_primitive = """ SELECT id FROM primitives WHERE name = %s;"""

sql_insert_song_primitive = """ INSERT INTO song_primitive(song_id, primitive_id, value) VALUES(%s,%s,%s); """


def connect():
    """ Connect to the PostgreSQL database server """
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        global conn
        conn = psycopg2.connect(**params)
        conn.autocommit = True

        # create a cursor
        global cur
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def disconnect():
    """ Disconnect to the PostgreSQL database server """
    try:
        # close the communication with the PostgreSQL
        if cur is not None:
            cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def insert_song(title, artist, id_genre):
    try:
        # INSERT song
        cur.execute(sql_insert_song, (title, artist, id_genre))

        # get the generated id back
        id_song = cur.fetchone()[0]
        return id_song

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        cur.execute("ROLLBACK")
        return False

def song_exists(title, artist):
    try:
        # INSERT genre
        cur.execute(sql_exist_song, (title, artist))
        
        # get the generated id back
        num_songs = cur.fetchone()[0]

        return num_songs > 0

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        cur.execute("ROLLBACK")
        return False

def insert_genre(genre):
    try:
        # INSERT genre
        cur.execute(sql_insert_genre, (genre,))
        
        # get the generated id back
        id_genre = cur.fetchone()[0]

        return id_genre

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        cur.execute("ROLLBACK")
        return False

def get_num_genres():
    try:
        # INSERT genre
        cur.execute(sql_count_genre)
        
        # get the generated id back
        num_genres = cur.fetchone()[0]

        return num_genres

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        cur.execute("ROLLBACK")
        return False

def insert_primitive(primitive):
    # SELECT id if primitive already exists
    try:
        cur.execute(sql_select_primitive, (primitive,))
        id_primitive = cur.fetchone()[0]

        if id_primitive is not None:
            return id_primitive

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    try:
        # INSERT primitive
        cur.execute(sql_insert_primitive, (primitive,))

        # get the generated id back
        id_primitive = cur.fetchone()[0]

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        cur.execute("ROLLBACK")

def insert_song_primitive(id_song, primitive, value):
    # retrieve primitive ID
    id_primitive = insert_primitive(primitive)

    try:
        cur.execute(sql_insert_song_primitive, (id_song, id_primitive, value))

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        cur.execute("ROLLBACK")

def populate_database(num_genres, songs_per_genre):
    if (not num_genres.isdigit() or not songs_per_genre.isdigit()):
        # TODO: Change to return code 400 (Bad request)
        print("Wrong parameter types")
        return False
    else:
        connect()
        print("---------------------")
        print("\n")

        genres_count = get_num_genres()
        genres = lastFM.get_genres(num_genres, genres_count)

        print(str(len(genres)) + " genres retrieved")

        genre_name_to_id = {}
        lastFM_songs = []
        for genre in genres:
            # add to database
            genre_id = insert_genre(genre)
            # keep a mapping of the genre's ID and its name
            if (genre_id is not False):
                genre_name_to_id[genre] = genre_id

            # extraction
            extraction = lastFM.get_songs_per_genre(genre, [], 1, songs_per_genre)
            lastFM_songs = lastFM_songs + extraction

        print(str(len(lastFM_songs)) + " songs retrieved")

        print("")
        print("Step 2 --- Spotify extraction")
        numSongs = 0
        for song in lastFM_songs:
            # get informations from Spotify API
            s = spotifyAPI.search_song(song['title'], song['artist'])
            if (s is not False):
                s['genre'] = song['genre']
                if s['genre'] in genre_name_to_id:
                    # add song to database
                    id_song = insert_song(s['title'], s['artist'], genre_name_to_id[s['genre']])
                    if (id_song is not False) :
                        # increment song count
                        numSongs = numSongs + 1
                        # insert primitives to database
                        for primitive, value in s['primitives'].items():
                            insert_song_primitive(id_song, primitive, value)

        print(str(numSongs) + " songs added")
        if (numSongs < len(lastFM_songs)):
            print(str(len(lastFM_songs) - numSongs) + " songs could not be added because of a duplicate issue.")
        
        print("\n")
        print("---------------------")
        disconnect()

