
# Spotify Vinyl Widget

A tiny, always-on-top Windows desktop widget that shows your currently playing Spotify track with a spinning circular album cover and simple controls (prev / play-pause / next).

**Backend:** Flask + Spotipy  
**Frontend:** HTML/CSS/JS  
**Desktop wrapper:** Electron

<img width="660" height="158" alt="image" src="https://github.com/user-attachments/assets/832ba9c2-edb7-41c3-a8b7-b98a7743723c" />


---

##  Features (v1.0.0)

- Circular album art that spins while music is playing
- Track title and artist(s)
- Play/Pause, Next, Previous buttons
- Auto-refresh every ~3.5s to stay in sync
- Always-on-top, frameless, draggable window on Windows (Electron)
- Clean neumorphic styling; transparent window background for “floating” look

> **Note:** Requires Spotify Premium for playback control (Spotify API limitation) and an active device (Spotify open on phone/desktop/web).

---

##  Architecture

- **Backend:** Flask web server, [spotipy](https://spotipy.readthedocs.io/) for Spotify Web API, [python-dotenv](https://pypi.org/project/python-dotenv/) for env loading
- **Frontend:** Single HTML file (`frontend.html`) with inline CSS/JS, talks to Flask via fetch
- **Desktop Wrapper:** Electron opens a small, transparent/frameless window pointing to the Flask URL

---

##  Requirements

- Python 3.8+
- Node.js (for Electron wrapper)
- Spotify Premium account

---

## 🚀 Setup

1. **Clone the repository:**
	```sh
	git clone https://github.com/jessmed749/spotify_vinyl_widget.git
	cd spotify_vinyl_widget
	```

2. **Install Python dependencies:**
	```sh
	pip install -r requirements.txt
	```

3. **Set up your `.env` file:**
	Create a `.env` file in the project root with your Spotify API credentials:
	```env
	SPOTIPY_CLIENT_ID=your_spotify_client_id
	SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
	SPOTIPY_REDIRECT_URI=http://localhost:8080/callback
	```

4. **Run the backend server:**
	```sh
	cd apps/python-widget
	python src/main.py
	```

5. **(Optional) Run the Electron desktop wrapper:**
	```sh
	# From the project root
	cd apps/electron-wrapper
	npm install
	npm start
	```

---

##  Usage

Open the Electron app or visit the Flask server URL in your browser. The widget will display your current Spotify track, album art, and controls.

---

## Contributing

Pull requests and suggestions are welcome! Please open an issue first to discuss changes.

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.


