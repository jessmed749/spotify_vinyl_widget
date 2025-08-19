
from __future__ import annotations
import tkinter as tk
import sp_client as sc  

POLL_MS = 2000

def normalize(playback):
    if not playback:
        return None
    if isinstance(playback, dict) and "title" in playback:
        return {"title": playback.get("title"),
                "artist": playback.get("artist", ""),
                "is_playing": bool(playback.get("is_playing"))}
    if isinstance(playback, dict) and "item" in playback:
        item = playback.get("item") or {}
        title = item.get("name")
        artists = ", ".join(a.get("name", "") for a in item.get("artists", [])) or ""
        is_playing = bool(playback.get("is_playing"))
        if title:
            return {"title": title, "artist": artists, "is_playing": is_playing}
    return None

class App(tk.Tk):
    def __init__(self, client: "sc.SpotifyClient"):
        super().__init__()
        self.client = client
        self.title("Spotify Widget")
        self.geometry("420x160")
        self.configure(bg="#111")
        self.title_var = tk.StringVar(value="—")
        self.artist_var = tk.StringVar(value="—")
        tk.Label(self, textvariable=self.title_var,
                 font=("Segoe UI", 16, "bold"),
                 fg="#eee", bg="#111", wraplength=380, anchor="w", justify="left").pack(
            padx=16, pady=(20, 4), anchor="w"
        )
        tk.Label(self, textvariable=self.artist_var,
                 font=("Segoe UI", 12),
                 fg="#aaa", bg="#111", wraplength=380, anchor="w", justify="left").pack(
            padx=16, pady=(0, 8), anchor="w"
        )
        self.after(0, self.refresh)

    def refresh(self):
        try:
            data = self.client.get_playback()
            track = normalize(data)
            if track:
                play_symbol = "▶" if track.get("is_playing") else "⏸"
                self.title_var.set(f"{track.get('title','Unknown')}  {play_symbol}")
                self.artist_var.set(track.get("artist", "Unknown artist"))
            else:
                self.title_var.set("Nothing playing")
                self.artist_var.set("—")
        except Exception as e:
            self.title_var.set("Error talking to Spotify")
            self.artist_var.set(str(e))
        self.after(POLL_MS, self.refresh)

if __name__ == "__main__":
    app = App(sc.SpotifyClient())
    app.mainloop()
