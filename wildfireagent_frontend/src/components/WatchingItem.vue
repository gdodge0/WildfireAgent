<script setup>
defineProps({
  name: {
    type: String,
    required: true
  },
  bg: {
    type: String,
    required: true
  },
  id: {
    type: String,
    required: true
  },

})
</script>

<template>
  <div :class="[bg, 'bg-opacity-100 hover:bg-opacity-80 px-6 py-2 flex flex-row justify-between items-center rounded-full']">
    <h2 class="text-white text-lg font-bold">{{ name }}</h2>
    <svg xmlns="http://www.w3.org/2000/svg" class="max-h-10" viewBox="0 -960 960 960" fill="#e8eaed">
      <path d="M504-480 320-664l56-56 240 240-240 240-56-56 184-184Z"/>
    </svg>
  </div>
</template>

