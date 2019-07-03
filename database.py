import psycopg2
from config import config

sql_insert_song = """ INSERT INTO songs(title, artist, genre_id, album_id) VALUES(%s,%s,%s, 0) RETURNING id; """
sql_select_song = """ SELECT id FROM songs WHERE title = %s AND artist = %s;"""

sql_insert_genre = """ INSERT INTO genre(name, is_selected) VALUES(%s, true) RETURNING id;"""
sql_select_genre = """ SELECT id FROM genre WHERE name = %s;"""

sql_insert_primitive = """ INSERT INTO primitive(primitive) VALUES(%s) RETURNING id_primitive; """
sql_select_primitive = """ SELECT id_primitive FROM primitive WHERE primitive = %s;"""

sql_insert_song_primitive = """ INSERT INTO song_primitive(id_song, id_primitive, value) VALUES(%s,%s,%s); """


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

    return id_primitive


def insert_song_primitive(id_song, primitive, value):

    id_primitive = insert_primitive(primitive)

    try:
        cur.execute(sql_insert_song_primitive, (id_song, id_primitive, value))

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        cur.execute("ROLLBACK")


