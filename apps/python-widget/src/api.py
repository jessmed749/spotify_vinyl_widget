
from flask import Flask, request, jsonify
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)
sp = Spotify(auth_manager=SpotifyOAuth(scope=(
    "user-read-playback-state user-modify-playback-state user-read-currently-playing"
)))

@app.get("/now")
def now():
    cp = sp.current_user_playing_track()
    state = sp.current_playback()
    if not cp or not cp.get("item"):
        return jsonify({"playing": False, "reason": "No track"}), 200
    item = cp["item"]
    return jsonify({
        "playing": cp.get("is_playing", False),
        "song": item["name"],
        "artists": ", ".join(a["name"] for a in item["artists"]),
        "album": item["album"]["name"],
        "album_image": item["album"]["images"][0]["url"] if item["album"]["images"] else None,
        "progress_ms": cp.get("progress_ms"),
        "duration_ms": item["duration_ms"],
        "device": (state or {}).get("device", {}),
        "shuffle_state": (state or {}).get("shuffle_state"),
        "repeat_state": (state or {}).get("repeat_state"),
    })

@app.post("/play")
def _play():
    sp.start_playback()
    return ("", 204)
@app.post("/pause")
def _pause():
    sp.pause_playback()
    return ("", 204)
@app.post("/next")
def _next():
    sp.next_track()
    return ("", 204)
@app.post("/prev")
def _prev():
    sp.previous_track()
    return ("", 204)

@app.post("/seek")
def _seek():
    ms = int(request.json.get("ms", 0))
    sp.seek_track(ms); return ("", 204)

@app.post("/volume")
def _vol():
    pct = max(0, min(100, int(request.json.get("percent", 50))))
    sp.volume(pct); return ("", 204)

if __name__ == "__main__":
    app.run(port=5057, debug=True)