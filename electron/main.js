const {app, BrowserWindow, ipcMain} = require("electron");
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
    speaker = utils.spawnWorker("speak");

    speaker.stderr.on("data", (data) => {
        console.log(`stderr: ${data}`);
    });

    speaker.stdout.on("data", (data) => {
        const message = data.toString().trim();
        console.log(message);

        if (message == "[READY]") {
            console.log("speaker is ready");
            mainWindow?.webContents.send("speaker-ready", 1);
        }
    });

    speaker.on("close", (code) => {
        console.log(`child process exited with code ${code}`);
    });

    return {speaker: speaker};
}

app.whenReady().then(() => {
    workers = createWorkers();
    createWindow();

    ipcMain.handle("speak", (event, text) => {
        cmd = `[SPEAK] ${text}`;
        workers.speaker.stdin.write(cmd + "\n");
    });

    // mac os - re-create window when dock icon is clicked and no other windows are open
    app.on("activate", function () {
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
});

app.on("window-all-closed", function () {
    if (process.platform !== "darwin") app.quit();
});
