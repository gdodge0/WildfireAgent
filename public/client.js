function getBase64(file) {
   var reader = new FileReader();
   reader.readAsDataURL(file);
   reader.onload = function () {
       window.MediaFileB64 = reader.result;
   };
   reader.onerror = function (error) {
     console.log('Error: ', error);
   };
}


function getLocalStream() {
  navigator.mediaDevices
    .getUserMedia({ video: false, audio: true })
    .then((stream) => {
      window.localStream = stream;
    })
    .catch((err) => {
      console.error(`you got an error: ${err}`);
    });
}

function toggle_recording() {
    let btn = document.getElementById("record-audio")
    if (window.recordedData){
        btn.className = "button-icon fa-solid fa-play"
        endRecording();
    } else {
        btn.className = "button-icon fa-solid fa-circle-notch"
        startRecording();
    }
}

function startRecording(){
    window.recordedData = [];
    window.mediaRecorder = new MediaRecorder(window.localStream,{mimeType: "audio/mp4"});
    window.mediaRecorder.ondataavailable = (event) => {
        window.recordedData.push(event.data);
    }
    window.mediaRecorder.onstop = (event) => {
        const blob = new Blob(window.recordedData, { type: "audio/mp4" });
        window.MediaFile = new File([blob], "recorded.mp4", {type: "audio/mp4"});
        window.recordedData=null;
        window.mediaRecorder = null;
        getBase64(window.MediaFile);
    }

    window.mediaRecorder.start();
}

function endRecording(){
    window.mediaRecorder.stop();
}

window.onload = function(){
    getLocalStream();
}



const PLAY_STATES = {
    NO_AUDIO: "no_audio",
    LOADING: "loading",
    PLAYING: "playing",
};

let playState = PLAY_STATES.NO_AUDIO;
let audioPlayer;
const errorMessage = document.querySelector("#error-message");
let audioChunks = []; // Array to buffer incoming audio data chunks
let socket;

// Function to update the play button based on the current state
function updatePlayButton() {
    const playButton = document.getElementById("play-button");
    const icon = playButton.querySelector(".button-icon");

    switch (playState) {
        case PLAY_STATES.NO_AUDIO:
            icon.className = "button-icon fa-solid fa-play";
            break;
        case PLAY_STATES.LOADING:
            icon.className = "button-icon fa-solid fa-circle-notch";
            break;
        case PLAY_STATES.PLAYING:
            icon.className = "button-icon fa-solid fa-stop";
            break;
        default:
            break;
    }
}

// Function to stop audio
function stopAudio() {
    audioPlayer = document.getElementById("audio-player");
    if (audioPlayer) {
        playState = PLAY_STATES.PLAYING;
        updatePlayButton();
        audioPlayer.pause();
        audioPlayer.currentTime = 0;
        audioPlayer = null;
    }
}

// Function to handle the click event on the play button
function playButtonClick() {
    switch (playState) {
        case PLAY_STATES.NO_AUDIO:
            sendData();
            break;
        case PLAY_STATES.PLAYING:
            stopAudio();
            playState = PLAY_STATES.NO_AUDIO;
            updatePlayButton();
            break;
        default:
            break;
    }
}

// Function to send data to backend via WebSocket
function sendData() {
    const modelSelect = document.getElementById("models");
    const fireID = document.getElementById('fire-id').value;
    if (!window.MediaFileB64) {
        errorMessage.innerHTML = "ERROR: Please add text!";
    } else {
        playState = PLAY_STATES.LOADING;
        updatePlayButton();

        // we want to simulate holding a connection open like you would for a websocket
        // that's the reason why we only initialize once
        if (!socket) {
            // create a new WebSocket connection
            socket = new WebSocket(`ws://localhost:3000`);

            // disable the model select
            modelSelect.disabled = true;

            socket.addEventListener("open", () => {
                const data = {
                    media: window.MediaFileB64,
                    session_id: "abf3ab05-91a0-4cdc-850e-8995a1cc9989"
                };
                socket.send(JSON.stringify(data));
            });

            socket.addEventListener("message", (event) => {
                // console.log("Incoming event:", event);

                if (typeof event.data === "string") {
                    console.log("Incoming text data:", event.data);

                    let msg = JSON.parse(event.data);

                    if (msg.type === "Open") {
                        console.log("WebSocket opened 2");
                    } else if (msg.type === "Error") {
                        console.error("WebSocket error:", error);
                        playState = PLAY_STATES.NO_AUDIO;
                        updatePlayButton();
                    } else if (msg.type === "Close") {
                        console.log("WebSocket closed");
                        playState = PLAY_STATES.NO_AUDIO;
                        updatePlayButton();
                    } else if (msg.type === "Flushed") {
                        console.log("Flushed received");

                        // All data received, now combine chunks and play audio
                        const blob = new Blob(audioChunks, { type: "audio/wav" });

                        if (window.MediaSource) {
                            console.log('MP4 audio is supported');
                            const audioContext = new AudioContext();
                    
                            const reader = new FileReader();
                            reader.onload = function () {
                                const arrayBuffer = this.result;
                    
                                audioContext.decodeAudioData(arrayBuffer, (buffer) => {
                                    const source = audioContext.createBufferSource();
                                    source.buffer = buffer;
                                    source.connect(audioContext.destination);
                                    source.start();
                    
                                    playState = PLAY_STATES.PLAYING;
                                    updatePlayButton();
                    
                                    source.onended = () => {
                                        // Clear the buffer
                                        audioChunks = [];
                                        playState = PLAY_STATES.NO_AUDIO;
                                        updatePlayButton();
                                    };
                                });
                            };
                            reader.readAsArrayBuffer(blob);
                        } else {
                            console.error('MP4 audio is NOT supported');
                        }
            
                        // Clear the buffer
                        audioChunks = [];
                    }
                }

                if (event.data instanceof Blob) {
                    // Incoming audio blob data
                    const blob = event.data;
                    console.log("Incoming blob data:", blob);

                    // Push each blob into the array
                    audioChunks.push(blob);
                }
            });
            
            socket.addEventListener("close", () => {
                console.log("Close received");
                playState = PLAY_STATES.NO_AUDIO;
                updatePlayButton();
            });

            socket.addEventListener("error", (error) => {
                console.error("WebSocket error:", error);
                playState = PLAY_STATES.NO_AUDIO;
                updatePlayButton();
            });
        } else {
            const data = {
                text: "",
            };
            socket.send(JSON.stringify(data));
        }
    }
}

// Event listener for the click event on the play button
document
    .getElementById("play-button")
    .addEventListener("click", playButtonClick);
