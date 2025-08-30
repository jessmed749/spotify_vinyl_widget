
import os
from flask import Flask, jsonify, request
from flask_cors import CORS

from sp_client import SpotifyClient

app = Flask(__name__, static_folder="web", static_url_path="/")
CORS(app)

client = SpotifyClient()

@app.get("/api/playback")   
def playback():
    data = client.sp.current_playback()
    if not data or not data.get("item"):
        return jsonify({"item": None})
    item = data["item"]
    tittle = item.get("name") or "Unknown"
    artists = ", ".join(a.get("name", "") for a in item.get("artists", [])) or "Unknown artist"
    images = item.get("album", {}).get("images", [])
    image = images[0]["url"] if images else None
    return jsonify({
        "item": {
            "title": tittle,
            "artist": artists,
            "is_playing": bool(data.get("is_playing")),
            "image": image,
        }
    })

@app.post("/api/play-pause")
def play_pause():
    pb = client.sp.current_playback()
    if pb and pb.get("is_playing"):
        client.sp.pause_playback()
    else:
        client.sp.start_playback()
    return "", 204

@app.post("/api/next")
def next_track():
    client.sp.next_track()
    return "", 204

@app.post("/api/previous")
def previous_track():
    client.sp.previous_track()
    return "", 204

@app.get("/")
def index():
    return app.send_static_file("index.html")

if __name__ == "__main__":
        app.run(host="127.0.0.1", port=int(os.getenv("API_PORT", 5057)), debug=True)

