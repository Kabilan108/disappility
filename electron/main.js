const { app, BrowserWindow, ipcMain } = require("electron");
const path = require("node:path");
const utils = require("./utils");

let mainWindow;

function createWindow() {
  // Create the browser window.
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      nodeIntegration: true,
      contextIsolation: true,
    },
  });

  // and load the index.html of the app.
  // mainWindow.loadFile("index.html");
  mainWindow.loadURL("http://localhost:3000");

  // Open the DevTools.
  mainWindow.webContents.openDevTools();
}

function createWorkers() {
  console.log("creating workers");
  let speaker = utils.spawnWorker("speak");
  let whisper = utils.spawnWorker("transcribe");
  let OI = utils.spawnWorker("openInterpreter");

  speaker.stderr.on("data", (data) => {
    console.log(`stderr: ${data}`);
  });

  whisper.stderr.on("data", (data) => {
    console.log(`stderr: ${data}`);
  });

  OI.stderr.on("data", (data) => {
    console.log(`stderr: ${data}`);
  });

  speaker.stdout.on("data", (data) => {
    const message = data.toString().trim();

    if (message == "[READY]") {
      console.log("speaker is ready");
      mainWindow?.webContents.send("speaker-ready", 1);
    }
  });

  whisper.stdout.on("data", (data) => {
    let message = data.toString().trim();

    console.log(`whisper: ${message}`);

    if (message == "[READY]") {
      console.log("whisper is ready");
      mainWindow?.webContents.send("whisper-ready", 1);
    }

    if (message.startsWith("[USERSAYS]")) {
      message = message.replace("[USERSAYS]", "[PROMPT]").trim(); // Use substitution to remove the "[USERSAYS]" token
      console.log(`${message}`);
      // speaker.stdin.write(`[SPEAK] working on it!`);
      OI.stdin.write(`[PROMPT] ${message}`);
    }
  });

  OI.stdout.on("data", (data) => {
    let message = data.toString().trim();
    console.log(`OI: ${message}`);
  });

  return { speaker: speaker, whisper: whisper, oi: OI };
}

app.whenReady().then(() => {
  workers = createWorkers();
  createWindow();

  // mac os - re-create window when dock icon is clicked and no other windows are open
  app.on("activate", function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on("window-all-closed", function () {
  if (process.platform !== "darwin") app.quit();
});
