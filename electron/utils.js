const { spawn } = require("child_process");
const path = require("path"); // Corrected import statement

function spawnWorker(type) {
  let workerPath;
  if (type === "speak") {
    workerPath = path.join(process.env.WORKER_DIR, "tts", "speak.py");
  } else if (type === "transcribe") {
<<<<<<< HEAD
    workerPath = path.join(process.env.WORKER_DIR, "whisper", "transcribe.py");
  } else if (type === "openInterpreter") {
    workerPath = path.join(process.env.WORKER_DIR, "openInterpreter", "oiProcessor.py");
=======
    workerPath = path.join(process.env.WORKER_DIR, "stt", "transcribe.py");
>>>>>>> cd926f6a426ad30c53ab4e374b1b8a3156858c5d
  }

  let command = `${process.env.PYTHON_PATH} ${workerPath}`;
  const worker = spawn(command, { shell: true });

  return worker;
}

module.exports = { spawnWorker };
