
import os
from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
#from spotipy.oauth2 import SpotifyClientCredentials #good for user data only

def main():
    load_dotenv()   #read env to not hardcore credentials
    
    # Initialize Spotify client with OAuth credentials
    sp = Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="user-library-read user-read-playback-state user-modify-playback-state",
    ))

    # Get current playing song
    current = sp.current_palying_track()

    if current and current.get('item'):
        song = current['item']["name"]
        artists = ', '.join(artist['name'] for artist in current['item']['artists'])
        print(f"Currently playing: {song} by {artists}")
    else:
        print("No track is currently playing.")

if __name__ == "__main__":
    main()