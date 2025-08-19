from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

def _sp():
    return Spotify(auth_manager=SpotifyOAuth(scope=(
        "user-read-playback-state user-modify-playback-state user-read-currently-playing"
    )))

def play(uri: str | None = None, device_id: str | None = None, position_ms: int | None = None):
    sp = _sp()
    if uri:
        sp.start_playback(device_id=device_id, uris=[uri], position_ms=position_ms)
    else:
        sp.start_playback(device_id=device_id)

def pause():
    _sp().pause_playback()

def next_track():
    _sp().next_track()

def prev_track():
    _sp().previous_track()

def set_volume(percent: int):
    _sp().volume(percent=max(0, min(100, percent)))

def seek(ms: int):
    _sp().seek_track(ms)

def transfer(device_id: str):
    _sp().transfer_playback(device_id=device_id, force_play=True)