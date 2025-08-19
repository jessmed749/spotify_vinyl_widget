import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

cliend_id = "your_client_id"
client_secret = "your_client_secret"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=cliend_id, client_secret=client_secret))

