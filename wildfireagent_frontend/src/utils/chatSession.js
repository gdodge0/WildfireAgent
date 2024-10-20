class ChatbotWebSocket {
  constructor(sessionId, baseUrl, isMicActiveRef, isTalkingRef, isLoadingRef) {
    this.sessionId = sessionId;
    this.baseUrl = baseUrl;
    this.isMicActiveRef = isMicActiveRef;
    this.isTalkingRef = isTalkingRef;
    this.isLoadingRef = isLoadingRef;


    this.socket = null;
    this.playState = 'no_audio';
    this.audioChunks = [];
    this.audioSource = null;
  }

  connect() {
    return new Promise((resolve, reject) => {
      if (!this.socket) {
        this.socket = new WebSocket(this.baseUrl);

        this.socket.addEventListener('open', () => {
          resolve();
        });

        this.socket.addEventListener('message', (event) => this.handleMessage(event));

        this.socket.addEventListener('close', () => {
          console.log('WebSocket closed');
          this.playState = 'no_audio';
        });

        this.socket.addEventListener('error', (error) => {
          console.error('WebSocket error:', error);
          reject(error);
        });
      } else {
        resolve();
      }
    });
  }

  handleMessage(event) {
    if (typeof event.data === 'string') {
      let msg = JSON.parse(event.data);
      console.log(msg)

      if (msg.type === 'Flushed') {
        console.log('Flushed received');
        this.playAudio();
      }
    }

    if (event.data instanceof Blob) {
      this.audioChunks.push(event.data);
    }
  }

  sendMessage(mediaFileB64) {
    const data = {
      media: mediaFileB64,
      session_id: this.sessionId,
    };
    this.socket.send(JSON.stringify(data));
  }
  sendMessageText(text) {
    const data = {
      text: text,
      session_id: this.sessionId,
    };
    this.socket.send(JSON.stringify(data));
  }
  playAudio() {
    this.isLoadingRef.value = false;
    // Only play the audio if the mic is active (isMicActiveRef is true)
    if (this.isMicActiveRef.value) {
      const blob = new Blob(this.audioChunks, { type: 'audio/wav' });
      const audioContext = new (window.AudioContext || window.webkitAudioContext)();
      const reader = new FileReader();
      this.isTalkingRef.value = true;
      reader.onload = () => {
        audioContext.decodeAudioData(reader.result).then((buffer) => {
          if (!this.isMicActiveRef.value) {
            return; // Do not play if the mic is toggled off before the audio starts
          }

          this.audioSource = audioContext.createBufferSource();
          this.audioSource.buffer = buffer;
          this.audioSource.connect(audioContext.destination);

          // Ensure the context is resumed if suspended
          if (audioContext.state === 'suspended') {
            audioContext.resume().then(() => {
              this.audioSource.start();
            });
          } else {
            this.audioSource.start();
          }

          this.playState = 'playing';

          // Stop the audio if the mic is toggled off mid-playback
          this.audioSource.onended = () => {
            if (this.isMicActiveRef.value) {
              this.playState = 'no_audio';
              this.isTalkingRef.value = false;
            }
          };
        });
      };
      reader.readAsArrayBuffer(blob);

       // Clear the audio chunks after playback

    } else {
      console.log('Audio will not be played because the mic is not active.');
    }
    this.audioChunks = [];
  }

  stopAudio() {
    // Stop the audio playback if the mic is toggled off early
    if (this.audioSource) {
      this.audioSource.stop();
      this.audioSource = null;
      this.playState = 'no_audio';
    }
  }

  close() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }
}

export default ChatbotWebSocket;
