const { app, BrowserWindow } = require('electron');

function createWindow() {
  const win = new BrowserWindow({
    width: 600,
    height: 400
  });

  win.setMenu(null);
  win.loadFile('index.html'); // Load your HTML frontend
}

app.whenReady().then(createWindow);
