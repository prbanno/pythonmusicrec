import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# Spotify API credentials
client_id = '58c8a93cb0384fa29e553bd21052e458'
client_secret = '70da00ea6de24e0e92df1cfb4c6a2ed0'

# Initialize Spotipy client
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Function to get top tracks by year
def get_top_tracks(year):
    top_tracks = sp.search(q=f'year:{year}', type='track', limit=50)
    return top_tracks['tracks']['items']


def extract_features(track):
    features = {
        'name': track['name'],
        'artist': track['artists'][0]['name'],
        'album': track['album']['name'],
        'album_cover': track['album']['images'][0]['url'],
       
    }
    return features


def get_audio_features(track_id):
    audio_features = sp.audio_features(track_id)
    if audio_features:
        return audio_features[0]  
    else:
        return None


def fetch_top_tracks(start_year, end_year):
    all_tracks = []
    for year in range(start_year, end_year + 1):
        tracks = get_top_tracks(year)
        for track in tracks:
            track_features = extract_features(track)
            audio_features = get_audio_features(track['id'])
            if audio_features:
                track_features['acousticness'] = audio_features['acousticness']
                track_features['loudness'] = audio_features['loudness']
                artist_id = track['artists'][0]['id']
                track_features['genres'] = get_artist_genres(artist_id)
                all_tracks.append(track_features)
    return all_tracks

# Function to get genres of an artist
def get_artist_genres(artist_id):
    artist_info = sp.artist(artist_id)
    artist_genres = artist_info['genres']
    return artist_genres

# Fetch top tracks from 2022 to 2024
start_year = 2022
end_year = 2024
top_tracks = fetch_top_tracks(start_year, end_year)

# Convert to DataFrame
df = pd.DataFrame(top_tracks)

# Print the entire DataFrame
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(df)
