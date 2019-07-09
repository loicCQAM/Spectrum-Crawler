import sys
import lastFM
import spotifyAPI
import json
import database

# Number of genres, Number of songs per genre
database.populate_database(sys.argv[1], sys.argv[2])
