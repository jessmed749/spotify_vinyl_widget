
import os
from pathlib import Path
from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

SCOPES = "user-read-currently-playing user-read-playback-state user-modify-playback-state"

def _load_env():
    env_path = Path(__file__).resolve().parents[1] / ".env"
    load_dotenv(env_path) 

# Initialize Spotify client with OAuth credentials
class SpotifyClient:
    def __init__(self):
        _load_env()
        self.sp = Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI", "http://localhost:8080/callback"),
            scope=SCOPES,
        ))

    # Get current playing song
    #current = sp.current_user_playing_track()


    def get_playback(self):
        data = self.sp.current_user_playing_track()
        if not data or not data.get("item"):
            return None
        item = data["item"]
        title = item.get("name")
        artists = ", ".join(a.get("name", "") for a in item.get("artists", []))
        return {
            "title": title or "Unknown",
            "artist": artists or "Unknown artist",
            "is_playing": bool(data.get("is_playing")),
        }

    def play_pause(self):
        pb = self.sp.current_playback()
        if pb and pb.get("is_playing"):
            self.sp.pause_playback()
        else:
            self.sp.start_playback()

    def next_track(self):
        self.sp.next_track()

if __name__ == "__main__":
    c = SpotifyClient()
    t = c.get_playback()
    print(f"Currently playing: {t['title']} by {t['artist']}") if t else print("No track is currently playing.")