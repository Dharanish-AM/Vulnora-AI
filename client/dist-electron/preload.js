import { contextBridge, ipcRenderer } from "electron";
contextBridge.exposeInMainWorld("electronAPI", {
  /**
   * Open a directory picker dialog
   * @returns {Promise<string|null>} Selected directory path or null if canceled
   */
  selectDirectory: () => ipcRenderer.invoke("select-directory"),
  /**
   * Check if the Python server is healthy
   * @returns {Promise<boolean>} True if server is running and healthy
   */
  checkServerHealth: () => ipcRenderer.invoke("check-server-health"),
  /**
   * Get the Python server URL
   * @returns {Promise<string>} Server URL
   */
  getServerUrl: () => ipcRenderer.invoke("get-server-url"),
  /**
   * Check if running in Electron
   * @returns {boolean} Always true in Electron context
   */
  isElectron: () => true
});
console.log("Preload script loaded successfully");
