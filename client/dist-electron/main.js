import { app, BrowserWindow, ipcMain, dialog } from "electron";
import path from "path";
import { fileURLToPath } from "url";
const __filename$1 = fileURLToPath(import.meta.url);
const __dirname$1 = path.dirname(__filename$1);
let mainWindow;
const PYTHON_SERVER_PORT = 8e3;
const PYTHON_SERVER_HOST = "localhost";
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1200,
    minHeight: 700,
    webPreferences: {
      preload: path.join(__dirname$1, "preload.js"),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: false
    },
    title: "Vulnora AI - Security Scanner",
    backgroundColor: "#ffffff",
    show: false
    // Don't show until ready
  });
  mainWindow.once("ready-to-show", () => {
    mainWindow.show();
  });
  if (process.env.VITE_DEV_SERVER_URL) {
    mainWindow.loadURL(process.env.VITE_DEV_SERVER_URL);
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(path.join(__dirname$1, "../dist/index.html"));
  }
  mainWindow.on("closed", () => {
    mainWindow = null;
  });
}
async function checkServerHealth() {
  try {
    const response = await fetch(`http://${PYTHON_SERVER_HOST}:${PYTHON_SERVER_PORT}/health`);
    return response.ok;
  } catch (error) {
    return false;
  }
}
app.whenReady().then(() => {
  createWindow();
  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});
app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});
ipcMain.handle("select-directory", async () => {
  const result = await dialog.showOpenDialog(mainWindow, {
    properties: ["openDirectory"],
    title: "Select Project Directory to Scan"
  });
  if (result.canceled) {
    return null;
  }
  return result.filePaths[0];
});
ipcMain.handle("check-server-health", async () => {
  return await checkServerHealth();
});
ipcMain.handle("get-server-url", () => {
  return `http://${PYTHON_SERVER_HOST}:${PYTHON_SERVER_PORT}`;
});
