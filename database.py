import psycopg2
import lastFM
import spotifyAPI
import math
from config import config
import sys


# SQL REQUESTS
sql_insert_song = """ INSERT INTO songs(title, artist, genre_id) VALUES(%s,%s,%s) RETURNING id; """
sql_update_song = """UPDATE songs SET album = %s, art = %s, sound = %s WHERE title = %s AND artist = %s RETURNING id; """
sql_select_song = """ SELECT id FROM songs WHERE title = %s AND artist = %s;"""
sql_exist_song = """ SELECT COUNT(id) FROM songs WHERE title = %s AND artist = %s;"""
sql_count_songs_genre = """ SELECT COUNT(id) FROM songs WHERE genre_id = %s;"""

sql_insert_genre = """ INSERT INTO genres(name, is_selected) VALUES(%s, true) RETURNING id;"""
sql_select_genre = """ SELECT id FROM genres WHERE name = %s;"""
sql_select_genre_id = """ SELECT id, name FROM genres WHERE id = %s;"""
sql_count_genre = """ SELECT COUNT(id) FROM genres;"""
sql_genre_exists = """ SELECT COUNT(id) FROM genres WHERE name = %s;"""

sql_insert_primitive = """ INSERT INTO primitives(name, is_selected) VALUES(%s, true) RETURNING id; """
sql_select_primitive = """ SELECT id FROM primitives WHERE name = %s;"""

sql_insert_song_primitive = """ INSERT INTO song_primitive(song_id, primitive_id, value) VALUES(%s,%s,%s); """


# DATABASE
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


# GENRES
def genre_exists(name):
    try:
        cur.execute(sql_genre_exists, (name, ))
        
        # get the generated id back
        num_genre = cur.fetchone()[0]
        return num_genre > 0

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        cur.execute("ROLLBACK")
        return False

def get_genre(id):
    try:
        cur.execute(sql_select_genre_id, (id,))
        
        # get the generated id back
        genre_id = cur.fetchone()
        return genre_id

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        cur.execute("ROLLBACK")
        return False

def get_genre_id_from_name(name):
    try:
        cur.execute(sql_select_genre, (name,))
        
        # get the generated id back
        genre_id = cur.fetchone()[0]
        return genre_id

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        cur.execute("ROLLBACK")
        return False

def insert_genre(genre):
    try:
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
        cur.execute(sql_count_genre)
        
        # get the generated id back
        num_genres = cur.fetchone()[0]

        return num_genres

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        cur.execute("ROLLBACK")
        return False


# SONGS
def song_exists(title, artist):
    try:
        cur.execute(sql_exist_song, (title, artist))
        # get the generated id back
        num_songs = cur.fetchone()[0]
        return num_songs > 0

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        cur.execute("ROLLBACK")
        return False

def insert_song(title, artist, id_genre):
    try:
        cur.execute(sql_insert_song, (title, artist, id_genre))

        # get the generated id back
        id_song = cur.fetchone()[0]
        return id_song

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        cur.execute("ROLLBACK")
        return False

def update_song(title, artist, album, art, sound):
    try:
        cur.execute(sql_update_song, (album, art, sound, title, artist))

        # get the generated id back
        id_song = cur.fetchone()[0]
        return id_song

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        cur.execute("ROLLBACK")
        return False

def count_songs_per_genre(genre_id):
    try:
        cur.execute(sql_count_songs_genre, (genre_id, ))
        num_songs = cur.fetchone()[0]
        return num_songs

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        cur.execute("ROLLBACK")
        return False

def convert_from_spotify(song):
    try:
        s = spotifyAPI.search_song(song['title'], song['artist'])
        if (s is not False):
            return s
    except:
        print("Error in Spotify convertion")


# PRIMITIVES
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


# MAIN FUNCTIONS
def populate_database(num_genres, songs_per_genre):
    """
    Description
    ----------
    Adds a given number of genre and a given number of songs for every genre.
    1) Retrieve the genres from LastFM API
    2) Loop genres, retrieve songs from LastFM API and add them to the database
    3) Loop songs, retrieve additional information from Spotify API and update in the database
    4) For every song, add primitives to the database

    Parameters
    ----------
    num_genres : int
        The number of genres to add
    songs_per_genre : int
        The number of songs to add for each genre
    """

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

        totalSongs = 0
        for genre in genres:
            numSongs = 0
            # add to database
            genre_id = insert_genre(genre)
            # keep a mapping of the genre's ID and its name
            if (genre_id is not False):
                # extraction
                lastFM_songs = lastFM.get_songs_per_genre(genre, genre_id, [], 1, songs_per_genre)

                # add Spotify information
                for song in lastFM_songs:
                    s = convert_from_spotify(song)
                    s['genre'] = genre
                    if (s is not False):
                        # update song with Spotify values in DB here
                        id_song = update_song(s['title'], s['artist'], s['album'], s['art'], s['sound'])
                        if (id_song is not False) :
                            # increment song count
                            numSongs = numSongs + 1    
                            # insert primitives to database
                            for primitive, value in s['primitives'].items():
                                insert_song_primitive(id_song, primitive, value)
                                    
                totalSongs = totalSongs + numSongs
                print(str(numSongs) + " songs added in " + genre)

        print(str(totalSongs) + " songs added in total.")

        disconnect()

def add_songs_to_genre(genre, songs_per_genre):
    """
    Description
    ----------
    Adds a given number of songs for a given genre name.
    1) Check if the genre is already in the database
    2) If the genre isn't in the database, retrieve it from the LastFM API and insert it
    3) Retrieve songs from LastFM API for the given genre and add them to the database
    4) Loop songs, retrieve additional information from Spotify API and update in the database
    5) For every song, add primitives to the database

    Parameters
    ----------
    genre : str
        The name of the genre
    songs_per_genre : int
        The number of songs to add for the specified genre
    """

    if (not type(genre) is str or not songs_per_genre.isdigit()):
        # TODO: Change to return code 400 (Bad request)
        print("Wrong parameter types")
        return False
    else:
        connect()
        numSongs = 0
        inDB = genre_exists(genre)

        if (not inDB):
            print("Not in Database !")
            if (lastFM.genre_exists(genre) is True) :
                genre_id = insert_genre(genre)
                page = 0
            else: 
                sys.exit("Error: Unvalid genre name.")
        else:
            genre_id = get_genre_id_from_name(genre)
            count = count_songs_per_genre(id)
            page = math.ceil(count/50)

        lastFM_songs = lastFM.get_songs_per_genre(genre, genre_id, [], page, songs_per_genre)

        # add Spotify information
        for song in lastFM_songs:
            s = convert_from_spotify(song)
            s['genre'] = genre
            if (s is not False):
                # update song with Spotify values in DB here
                id_song = update_song(s['title'], s['artist'], s['album'], s['art'], s['sound'])
                if (id_song is not False) :
                    # increment song count
                    numSongs = numSongs + 1    
                    # insert primitives to database
                    for primitive, value in s['primitives'].items():
                        insert_song_primitive(id_song, primitive, value)
                            
        print(str(numSongs) + " songs added in " + genre)

        disconnect()