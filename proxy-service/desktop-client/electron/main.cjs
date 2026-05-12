const { app, BrowserWindow, shell } = require('electron')
const path = require('path')

const isDev = Boolean(process.env.VITE_DEV_SERVER_URL)

function createWindow() {
  const window = new BrowserWindow({
    width: 1180,
    height: 840,
    minWidth: 980,
    minHeight: 720,
    backgroundColor: '#0b1020',
    title: 'Proxy Desktop Client',
    titleBarStyle: process.platform === 'darwin' ? 'hiddenInset' : 'default',
    webPreferences: {
      preload: path.join(__dirname, 'preload.cjs'),
      contextIsolation: true,
      nodeIntegration: false
    }
  })

  window.removeMenu()

  window.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url)
    return { action: 'deny' }
  })

  if (isDev) {
    window.loadURL(process.env.VITE_DEV_SERVER_URL)
  } else {
    window.loadFile(path.join(__dirname, '..', 'dist', 'index.html'))
  }
}

app.whenReady().then(() => {
  createWindow()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})
