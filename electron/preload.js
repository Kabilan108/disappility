const { contextBridge, ipcRenderer } = require("electron/renderer");

contextBridge.exposeInMainWorld("electron", {
  onSpeakerReady: (callback) =>
    ipcRenderer.on("speaker-ready", (_event, value) => callback(value)),
  speak: (text) => ipcRenderer.invoke("speak", text),
});
