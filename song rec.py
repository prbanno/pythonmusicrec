import pandas as pd


import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API credentials

# Initialize Spotipy with client credentials
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'

# Get albums for the artist
results = sp.artist_albums(birdy_uri, album_type='album')
albums = results['items']

# Retrieve all albums (if there are more than 20)
while results['next']:
    results = sp.next(results)
    albums.extend(results['items'])

# Print album names
for album in albums:
    print(album['name'])
