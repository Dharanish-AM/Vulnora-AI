import { app, BrowserWindow, ipcMain, dialog } from 'electron';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

let mainWindow;

// Python server configuration
const PYTHON_SERVER_PORT = 8000;
const PYTHON_SERVER_HOST = 'localhost';

/**
 * Create the main application window
 */
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1200,
    minHeight: 700,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: false,
    },
    title: 'Vulnora AI - Security Scanner',
    backgroundColor: '#ffffff',
    show: false, // Don't show until ready
  });

  // Show window when ready to avoid flickering
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  // Load the app
  if (process.env.VITE_DEV_SERVER_URL) {
    // Development mode
    mainWindow.loadURL(process.env.VITE_DEV_SERVER_URL);
    mainWindow.webContents.openDevTools();
  } else {
    // Production mode
    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'));
  }

  // Handle window close
  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

/**
 * Check if Python server is running
 */
async function checkServerHealth() {
  try {
    const response = await fetch(`http://${PYTHON_SERVER_HOST}:${PYTHON_SERVER_PORT}/health`);
    return response.ok;
  } catch (error) {
    return false;
  }
}

// App lifecycle events
app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// IPC Handlers
ipcMain.handle('select-directory', async () => {
  const result = await dialog.showOpenDialog(mainWindow, {
    properties: ['openDirectory'],
    title: 'Select Project Directory to Scan',
  });
  
  if (result.canceled) {
    return null;
  }
  
  return result.filePaths[0];
});

ipcMain.handle('check-server-health', async () => {
  return await checkServerHealth();
});

ipcMain.handle('get-server-url', () => {
  return `http://${PYTHON_SERVER_HOST}:${PYTHON_SERVER_PORT}`;
});

