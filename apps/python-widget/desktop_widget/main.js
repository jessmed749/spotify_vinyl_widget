const { app, BrowserWindow, Tray, Menu, globalShortcut } = require("electron");
const path = require("path");

let win, tray;

function createWindow() {
  win = new BrowserWindow({
    width: 720,
    height: 200,
    frame: false,            // no title bar: widget feel
    transparent: true,       // rounded card floats
    resizable: false,
    alwaysOnTop: true,       // keep above other windows
    backgroundColor: "#00000000",
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false
    }
  });

  // LoadFlask-served page so API_BASE='' works (same origin)
  win.loadURL("http://127.0.0.1:5057/");

  // ESC to close
  win.webContents.on("before-input-event", (e, input) => {
    if (input.key === "Escape") win.close();
  });
}

function createTray() {
  tray = new Tray(path.join(__dirname, "icon.ico")); // put an icon here :)
  const contextMenu = Menu.buildFromTemplate([
    { label: "Show/Hide", click: () => (win.isVisible() ? win.hide() : win.show()) },
    { type: "separator" },
    { label: "Quit", click: () => app.quit() }
  ]);
  tray.setToolTip("Spotify Widget");
  tray.setContextMenu(contextMenu);
  tray.on("click", () => (win.isVisible() ? win.hide() : win.show()));
}

app.whenReady().then(() => {
  createWindow();
  try { globalShortcut.register("Ctrl+Shift+W", () => (win.isVisible() ? win.hide() : win.show())); } catch {}
  try { createTray(); } catch {}
  app.on("activate", () => { if (BrowserWindow.getAllWindows().length === 0) createWindow(); });
});

app.on("window-all-closed", () => app.quit());