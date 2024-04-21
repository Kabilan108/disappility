const { contextBridge, ipcRenderer } = require("electron/renderer");

contextBridge.exposeInMainWorld("electron", {
  onSpeakerReady: (callback) =>
    ipcRenderer.on("speaker-ready", (_event, value) => callback(value)),
  onWhisperReady: (callback) =>
    ipcRenderer.on("whisper-ready", (_event, value) => callback(value)),
  onUserSays: (callback) =>
    ipcRenderer.on("user-says", (_event, value) => callback(value)),
});
