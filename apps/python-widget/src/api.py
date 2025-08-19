
from flask import Flask, jsonify, request
from flask_cors import CORS
from spotipy.exceptions import SpotifyException

try:
    from spotify_client import SpotifyClient
except ImportError:
    from sp_client import SpotifyClient

app = Flask(__name__)
CORS(app)

spc = SpotifyClient()   

def _ok(data=None, code=200):
    return (jsonify(data or {}), code)

def _err(msg, code=400):
    return (jsonify({"error": msg}), code)

@app.get("/now")
def now():
    try:
        cur = spc.sp.current_user_playing_track()
        state = spc.sp.current_playback()
        if not cur or not cur.get("item"):
            return _ok({
                "playing": False,
                "reason": "No track",
                "device": (state or {}).get("device", None),
            })
        item = cur["item"]
        return _ok({
            "playing": bool(cur.get("is_playing")),
            "title": item.get("name"),
            "artists": ", ".join(a.get("name", "") for a in item.get("artists", [])),
            "album": item.get("album", {}).get("name"),
            "album_image": (item.get("album", {}).get("images") or [{}])[0].get("url"),
            "progress_ms": cur.get("progress_ms"),
            "duration_ms": item.get("duration_ms"),
            "device": (state or {}).get("device", None),
            "shuffle_state": (state or {}).get("shuffle_state"),
            "repeat_state": (state or {}).get("repeat_state"),
        })
    except SpotifyException as e:
        return _err(str(e), 409)

@app.post("/playpause")
def playpause():
    try:
        spc.play_pause()
        return ("", 204)
    except SpotifyException as e:
        return _err(str(e), 409)

@app.post("/next")
def next_track():
    try:
        spc.next_track()
        return ("", 204)
    except SpotifyException as e:
        return _err(str(e), 409)

@app.post("/seek")
def seek():
    try:
        ms = int(request.json.get("ms", 0))
        spc.sp.seek_track(ms)
        return ("", 204)
    except (ValueError, TypeError):
        return _err("ms must be an integer", 400)
    except SpotifyException as e:
        return _err(str(e), 409)

@app.post("/volume")
def volume():
    try:
        pct = max(0, min(100, int(request.json.get("percent", 50))))
        spc.sp.volume(pct)
        return ("", 204)
    except (ValueError, TypeError):
        return _err("percent must be 0..100", 400)
    except SpotifyException as e:
        return _err(str(e), 409)

@app.get("/devices")
def devices():
    try:
        return _ok(spc.sp.devices().get("devices", []))
    except SpotifyException as e:
        return _err(str(e), 409)

@app.post("/transfer")
def transfer():
    try:
        device_id = request.json["device_id"]
        spc.sp.transfer_playback(device_id, force=True)
        return ("", 204)
    except KeyError:
        return _err("device_id is required", 400)
    except SpotifyException as e:
        return _err(str(e), 409)

if __name__ == "__main__":
    # run: .\.venv\Scripts\python .\src\api.py
    app.run(host="127.0.0.1", port=int(os.getenv("API_PORT", 5057)), debug=True)