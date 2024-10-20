<script setup>
import { ref, nextTick, onMounted, onBeforeUnmount } from 'vue';
import ChatbotWebSocket from '../utils/chatSession.js'; // Assuming the WebSocket class is in the same folder

const props = defineProps({
  id: {
    type: String,
    required: true
  },
  name: {
    type: String,
    required: true
  },
  session_id: {
    type: String,
    required: true
  }
});
const chatMessages = ref([
  { sender: 'bot', text: `Hello, what would you like to know about the ${props.name}?` }
]);
const isMicActive = ref(false);
const isRecording = ref(false); // To handle recording state
const isButtonDisabled = ref(false); // To disable button after release
const mediaRecorder = ref(null); // Reference for MediaRecorder
const chatContainer = ref(null);
const recordedChunks = ref([]); // Store audio data
const isLoading = ref(false);
const isTalking = ref(false);
const userInput = ref('');
let ws; // WebSocket instance

// Toggle microphone state
const toggleMic = () => {
  isMicActive.value = !isMicActive.value;
  isLoading.value = false;
  isTalking.value = false;
  if (!isMicActive.value && ws) {
    ws.stopAudio(); // Stop the audio if the mic is toggled off
  }
};

// Start recording when button is pressed
const startRecording = async () => {
  if (isButtonDisabled.value) return;

  // Request audio stream from the user's microphone
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  mediaRecorder.value = new MediaRecorder(stream);
  recordedChunks.value = [];

  mediaRecorder.value.ondataavailable = (event) => {
    if (event.data.size > 0) {
      recordedChunks.value.push(event.data);
    }
  };

  mediaRecorder.value.start();
  isRecording.value = true;
};

// Stop recording when button is released and send the audio
const stopRecording = () => {
  if (mediaRecorder.value && isRecording.value) {
    mediaRecorder.value.stop();
    mediaRecorder.value.onstop = async () => {
      const blob = new Blob(recordedChunks.value, { type: 'audio/mp4' });
      const reader = new FileReader();

      reader.onload = () => {
        const base64AudioMessage = reader.result;
        sendAudio(base64AudioMessage); // Send the audio message via WebSocket
      };

      reader.readAsDataURL(blob);
    };

    isRecording.value = false;
    isButtonDisabled.value = true; // Disable the button
  }
};

const toggleRecording = async () => {
  if (isButtonDisabled.value) return;

  if (!isRecording.value) {
    ws.stopAudio();
    await startRecording();
  } else {
    // Stop recording
    stopRecording();
  }
};

// Function to send audio via WebSocket
const sendAudio = (audioData) => {
  isLoading.value = true;
  if (ws) {
    ws.sendMessage(audioData); // Assuming WebSocket class has a method to send audio
  }
};

// Handle AI response and re-enable the button when done
const handleBotResponse = (response) => {
  // Add bot's response to the chat log
  chatMessages.value.push({
    sender: 'bot',
    text: response,
  });
  scrollToBottom();
  isButtonDisabled.value = false; // Re-enable the button after AI finishes talking
};

// Handle user text message input
const sendMessage = async (userMessage) => {
  if (userMessage.trim() !== '') {
    chatMessages.value.push({ sender: 'user', text: userMessage });
    if (ws) {
      ws.sendMessageText(userMessage); // Send user message via WebSocket
    }
    await scrollToBottom();
  }
};

// Scroll to the bottom of the chat container
const scrollToBottom = async () => {
  await nextTick(); // Ensure DOM updates first
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
  }
};

// Handle form input for sending text messages
const handleInputSubmit = () => {
  sendMessage(userInput.value);
  userInput.value = ''; // Clear the input after sending
};

// Initialize WebSocket connection when component mounts
onMounted(() => {
  ws = new ChatbotWebSocket(props.session_id, 'ws://localhost:3000', isMicActive, isTalking, isLoading);
  ws.connect()
    .then(() => {
      console.log('WebSocket connected');
    })
    .catch((err) => {
      console.error('WebSocket connection error:', err);
    });

  // Handle WebSocket message events
  ws.socket.addEventListener('message', (event) => {
    if (typeof event.data === 'string') {
      let msg = JSON.parse(event.data);
      if (msg.type !== 'Flushed') {
        if (msg.user_message_transcribed){
          chatMessages.value.push({ sender: 'user', text: msg.user_message_transcribed });
        }
        handleBotResponse(msg.ai_response);

      }
    }
  });
});

// Clean up WebSocket connection before the component is unmounted
onBeforeUnmount(() => {
  if (ws) {
    ws.close();
  }
});
</script>

<template>
  <div class="relative max-h-full h-full max-w-full w-full flex flex-col bg-transparent text-white justify-between items-stretch">
    <div ref="chatContainer" class="overflow-y-auto bg-transparent min-h-0">
      <div  v-for="(message, index) in chatMessages" :key="index" class="mb-4">
        <p v-if="message.sender === 'bot'" class="bg-gray-800 p-2 rounded-lg">
          {{ message.text }}
        </p>
        <p v-if="message.sender === 'user'" class="bg-gray-600 p-2 rounded-lg self-end">
          {{ message.text }}
        </p>
      </div>
    </div>
    <div class="flex flex-row justify-between items-center bg-transparent gap-x-4 max-w-full overflow-hidden min-h-[42px]">
      <div class="flex-grow flex flex-row justify-between items-center gap-x-2 bg-transparent border border-white text-white max-w-full rounded-full px-6 overflow-hidden">
        <div class="flex-grow overflow-hidden py-2">
          <input
            type="text"
            placeholder="Type your message..."
            v-model="userInput"
            @keydown.enter="handleInputSubmit"
            class=" bg-transparent focus:outline-none"/>
        </div>
        <button @click="handleInputSubmit" class="bg-transparent active:bg-white text-white active:text-black transition-all rounded-full p-2">
          <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="currentColor">
            <path d="M120-160v-640l760 320-760 320Zm80-120 474-200-474-200v140l240 60-240 60v140Zm0 0v-400 400Z"/>
          </svg>
        </button>
      </div>
      <button @click="toggleMic" class="bg-transparent border border-white text-white active:bg-white active:text-black transition-all p-2 rounded-full">
        <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="currentColor"><path d="M480-400q-50 0-85-35t-35-85v-240q0-50 35-85t85-35q50 0 85 35t35 85v240q0 50-35 85t-85 35Zm0-240Zm-40 520v-123q-104-14-172-93t-68-184h80q0 83 58.5 141.5T480-320q83 0 141.5-58.5T680-520h80q0 105-68 184t-172 93v123h-80Zm40-360q17 0 28.5-11.5T520-520v-240q0-17-11.5-28.5T480-800q-17 0-28.5 11.5T440-760v240q0 17 11.5 28.5T480-480Z"/></svg>
      </button>
    </div>
  </div>
  <div class="bg-red-500 rounded-t-2xl absolute left-0 bottom-0 w-screen margin-auto transition-all duration-300 flex flex-col justify-between items-stretch overflow-hidden"
    :class="isMicActive ? 'h-3/5' : 'h-0'">
    <div class="flex flex-row justify-start items-center p-2">
      <button @click="toggleMic" class="bg-transparent border border-white text-white active:bg-white active:text-red-500 transition-all p-2 rounded-full">
        <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="currentColor">
          <path d="M480-344 240-584l56-56 184 184 184-184 56 56-240 240Z"/>
        </svg>
      </button>
    </div>
    <div
      class="flex flex-row justify-center items-center gap-x-4"
      id="animated-bars"
    >
      <div :class="{'loading-bar': isLoading,'talking-bar': isTalking,}" class="bar"></div>
      <div :class="{'loading-bar': isLoading,'talking-bar': isTalking,}" class="bar"></div>
      <div :class="{'loading-bar': isLoading,'talking-bar': isTalking,}" class="bar"></div>
      <div :class="{'loading-bar': isLoading,'talking-bar': isTalking,}" class="bar"></div>
      <div :class="{'loading-bar': isLoading,'talking-bar': isTalking,}" class="bar"></div>

    </div>
    <div class="flex flex-col justify-center items-center py-6">
      <button
        @click="toggleRecording"
        :disabled="isButtonDisabled"
        :class="{'text-red-500 bg-white': isRecording, 'bg-transparent text-white': !isRecording}"
        class="rounded-full p-2 border-2 border-white transition-all duration-500 disabled:bg-red-300 disabled:border-gray-400 disabled:text-gray-400">
        <svg xmlns="http://www.w3.org/2000/svg" height="48px" class="max-h-15 h-15 min-h-15" viewBox="0 -960 960 960"  fill="currentColor">
          <path d="M480-400q-50 0-85-35t-35-85v-240q0-50 35-85t85-35q50 0 85 35t35 85v240q0 50-35 85t-85 35Zm0-240Zm-40 520v-123q-104-14-172-93t-68-184h80q0 83 58.5 141.5T480-320q83 0 141.5-58.5T680-520h80q0 105-68 184t-172 93v123h-80Zm40-360q17 0 28.5-11.5T520-520v-240q0-17-11.5-28.5T480-800q-17 0-28.5 11.5T440-760v240q0 17 11.5 28.5T480-480Z"/>
        </svg>
      </button>
      <span class="text-white font-medium">{{ isRecording ? 'Tap to send' : 'Tap to ask a question' }}</span>
    </div>
  </div>

</template>

<style scoped>
/* Additional styles if needed */
@keyframes undulate {
  0%, 100% {
    transform: scaleY(1); /* Default height */
  }
  20% {
    transform: scaleY(1.5); /* Peak height for forward */
  }
  50% {
    transform: scaleY(1); /* Back to default */
  }
  70% {
    transform: scaleY(1.5); /* Peak height for reverse */
  }
}
@keyframes talking-animate {
  0% {
    transform: scaleY(1); /* Default height */
  }
  20% {
    transform: scaleY(2); /* Taller bar */
  }
  40% {
    transform: scaleY(0.8); /* Shorter bar */
  }
  60% {
    transform: scaleY(1.7); /* Taller again */
  }
  80% {
    transform: scaleY(1.2); /* Medium height */
  }
  100% {
    transform: scaleY(1); /* Back to default */
  }
}
.bar {
  display: inline-block;
  width: 10px;
  height: 20px;
  background-color: white;
  margin: 0 5px;
  border-radius: 50%;
}

.loading-bar {

  animation: undulate 1.4s ease-in-out infinite; /* Continuous animation */
}
.talking-bar {
  animation: talking-animate 0.8s infinite;
}

.loading-bar:nth-child(1) { animation-delay: 0s; }
.loading-bar:nth-child(2) { animation-delay: 0.1s; }
.loading-bar:nth-child(3) { animation-delay: 0.2s; }
.loading-bar:nth-child(4) { animation-delay: 0.3s; }
.loading-bar:nth-child(5) { animation-delay: 0.4s; }

.talking-bar:nth-child(1) { animation-delay: 0.1s; }
.talking-bar:nth-child(2) { animation-delay: 0.15s; }
.talking-bar:nth-child(3) { animation-delay: 0.05s; }
.talking-bar:nth-child(4) { animation-delay: 0.2s; }
.talking-bar:nth-child(5) { animation-delay: 0.1s; }

</style>
