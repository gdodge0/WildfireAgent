<script setup>
import GoogleMap from "@/components/GoogleMap.vue";
import Chat from "@/components/Chat.vue";

import { ref, onMounted } from 'vue';
import axios from 'axios';

const props = defineProps({
  id: {
    type: String,
    required: true
  },
})

const fireSummary = ref(null);
const error = ref(null);

// Function to fetch the fire summary
const fetchFireSummary = async () => {
  try {
    const response = await axios.get('http://localhost:5000/api/v1/get_single_info', {
      params: {
        geo_id: props.id,
      },
    });
    fireSummary.value = response.data;
    console.log(response.data)
  } catch (err) {
    error.value = 'Failed to fetch fire information';
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
      <h2 class="text-white text-lg font-bold">Line Fire {{ id }}</h2>
      <button class="p-2 rounded-full bg-transparent text-white active:bg-white active:text-black transition-all">
        <svg xmlns="http://www.w3.org/2000/svg" class="max-h-10 h-8" viewBox="0 -960 960 960" fill="currentColor">
          <path d="M120-160v-640l760 320-760 320Zm80-120 474-200-474-200v140l240 60-240 60v140Zm0 0v-400 400Z"/>
        </svg>
      </button>
    </div>
    <div class="flex-grow grid grid-rows-3 justify-stretch items-stretch min-h-0 ">
      <div class="w-screen">
        <GoogleMap />
      </div>
      <div class="w-screen row-span-2 p-4">
        <Chat :id="id"/>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>