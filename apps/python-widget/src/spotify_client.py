
import os
from pathlib import Path
from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
#from spotipy.oauth2 import SpotifyClientCredentials #good for user data only


SCOPES = "user-read-currently-playing user-read-playback-state user-modify-playback-state"

def require(name: str) -> str:
    val = os.getenv(name)
    if not val:
        raise RuntimeError(f"Missing {name}. Check apps/python-widget/.env and your Spotify app settings.")
    return val

def main():
   #load_dotenv()   #read env to not hardcore credentials
    env_path = Path(__file__).resolve().parents[1] / ".env"
    load_dotenv(env_path)
    
    # Initialize Spotify client with OAuth credentials
    sp = Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI", "http://localhost:8080/callback"),
        scope="user-library-read user-read-playback-state user-modify-playback-state",
    ))

    # Get current playing song
    current = sp.current_user_playing_track()

    if current and current.get('item'):
        song = current['item']["name"]
        artists = ', '.join(artist['name'] for artist in current['item']['artists'])
        print(f"Currently playing: {song} by {artists}")
    else:
        print("No track is currently playing.")

if __name__ == "__main__":
    main()