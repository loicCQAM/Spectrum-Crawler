import sys
import lastFM
import spotifyAPI
import json
import database

database.populate_database(sys.argv[1], sys.argv[2])

