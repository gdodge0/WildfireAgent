class ChatbotWebSocket {
  constructor(sessionId, baseUrl) {
    this.sessionId = sessionId;
    this.baseUrl = baseUrl;
    this.socket = null;
    this.playState = 'no_audio';
    this.audioChunks = [];
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
      console.log(this.audioChunks);
    const blob = new Blob(this.audioChunks, { type: 'audio/wav' });
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const reader = new FileReader();

    reader.onload = function () {
        const arrayBuffer = this.result;
      audioContext.decodeAudioData(arrayBuffer, (buffer) => {
        const source = audioContext.createBufferSource();
        source.buffer = buffer;
        source.connect(audioContext.destination);
        source.start();
      });
    };
    reader.readAsArrayBuffer(blob);

    this.audioChunks = []; // Clear audio chunks after playing
  }

  close() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }
}

export default ChatbotWebSocket;
