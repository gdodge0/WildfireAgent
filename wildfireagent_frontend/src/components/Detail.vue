<script setup>
import GoogleMap from "@/components/GoogleMap.vue";
import Chat from "@/components/Chat.vue";

import { ref, onMounted, getCurrentInstance } from 'vue';
import axios from 'axios';

const props = defineProps({
  id: {
    type: String,
    required: true
  },
})

let session_id = ref(null);
const fire_name = ref(null);
let fireCoords = ref([]);

// Access global properties using getCurrentInstance()
const instance = getCurrentInstance()
const api_url = instance.appContext.config.globalProperties.$api_url
// Function to fetch the fire summary
const fetchFireSummary = async () => {
  try {
    const response = await axios.get(api_url+'/api/v1/start_chat_session', {
      params: {
        geo_id: props.id,
      },
    });
    fire_name.value = response.data.event_data.name;
    session_id.value = response.data.session_id;
    fireCoords.value.push({ lat: response.data.event_data.lat, lng: response.data.event_data.lng});

    console.log(response.data)
  } catch (err) {
    console.log(err);
  }
};

// Fetch the data when the component is mounted
onMounted(() => {
  fetchFireSummary();
});
</script>

<template>
  <div class="max-w-screen w-screen max-h-screen h-screen bg-neutral-900 flex flex-col justify-start items-stretch overflow-hidden">
    <div class="bg-red-500 p-2 flex flex-row justify-between items-center">
      <router-link to="/" class="p-2 rounded-full bg-transparent text-white active:bg-white active:text-black transition-all">
        <svg xmlns="http://www.w3.org/2000/svg" class="max-h-10 h-8" viewBox="0 -960 960 960" fill="currentColor">
          <path d="M560-240 320-480l240-240 56 56-184 184 184 184-56 56Z"/>
        </svg>
      </router-link>
      <h2 class="text-white text-lg font-bold" >{{ fire_name }}</h2>
      <button class="p-2 rounded-full bg-transparent text-white active:bg-white active:text-black transition-all">
        <svg xmlns="http://www.w3.org/2000/svg" class="max-h-10 h-8" viewBox="0 -960 960 960" fill="currentColor">
          <path d="M120-160v-640l760 320-760 320Zm80-120 474-200-474-200v140l240 60-240 60v140Zm0 0v-400 400Z"/>
        </svg>
      </button>
    </div>
    <div class="flex-grow grid grid-rows-3 justify-stretch items-stretch min-h-0 ">
      <div class="w-screen">
        <GoogleMap :fireCoordinates="fireCoords"/>
      </div>
      <div class="w-screen row-span-2 p-4">
        <Chat v-if="session_id" :id="props.id" :name="fire_name" :session_id="session_id" />
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>