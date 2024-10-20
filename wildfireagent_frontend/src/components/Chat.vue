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
const chatContainer = ref(null);
const userInput = ref('');
let ws; // Variable to hold the WebSocket instance

// Function to handle user message input
const sendMessage = async (userMessage) => {
  if (userMessage.trim() !== '') {
    // Add user's message to the chat log
    chatMessages.value.push({ sender: 'user', text: userMessage });

    // Send the message to the backend via WebSocket
    if (ws) {
      ws.sendMessageText(userMessage); // Sending user message to the WebSocket server
    }

    await scrollToBottom();
  }
};

// Function to scroll to the bottom of the chat container
const scrollToBottom = async () => {
  await nextTick(); // Ensure DOM updates first
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
  }
};

// Handle form input
const handleInputSubmit = () => {
  sendMessage(userInput.value);
  userInput.value = ''; // Clear the input after sending
};

// Function to handle incoming bot response
const handleBotResponse = (response) => {
  // Add bot's response to the chat log
  chatMessages.value.push({
    sender: 'bot',
    text: response,
  });
  scrollToBottom();
};

// Initialize WebSocket connection when component mounts
onMounted(() => {
  ws = new ChatbotWebSocket(props.session_id, 'ws://localhost:3000');
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
  <div class="max-h-full h-full max-w-full w-full flex flex-col bg-transparent text-white justify-between items-stretch">
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
      <div class="flex flex-row justify-between items-center gap-x-2 bg-transparent border border-white text-white max-w-full rounded-full px-6 overflow-hidden">
        <div class="overflow-hidden py-2">
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
      <button class="bg-transparent border border-white text-white active:bg-white active:text-black transition-all p-2 rounded-full">
        <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="currentColor"><path d="M480-400q-50 0-85-35t-35-85v-240q0-50 35-85t85-35q50 0 85 35t35 85v240q0 50-35 85t-85 35Zm0-240Zm-40 520v-123q-104-14-172-93t-68-184h80q0 83 58.5 141.5T480-320q83 0 141.5-58.5T680-520h80q0 105-68 184t-172 93v123h-80Zm40-360q17 0 28.5-11.5T520-520v-240q0-17-11.5-28.5T480-800q-17 0-28.5 11.5T440-760v240q0 17 11.5 28.5T480-480Z"/></svg>
      </button>
    </div>
  </div>
</template>

<style scoped>
/* Additional styles if needed */
</style>
