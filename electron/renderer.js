window.electron.onSpeakerReady((value) => {
  console.log("event received:", value);
  if (value === 1) {
    document.getElementById("generate-speech").style.display = "block";
  }
});

const speakButton = document.getElementById("speak-button");
speakButton.addEventListener("click", async () => {
  const text = document.getElementById("speech-input").value;
  await window.electron.speak(text);
});
