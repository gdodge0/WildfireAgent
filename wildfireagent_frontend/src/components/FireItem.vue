<script setup>
defineProps({
  name: {
    type: String,
    required: true
  },
  location: {
    type: String,
    required: true
  },
  containment: {
    type: String,
    required: true
  },
  size: {
    type: String,
    required: true
  },
  proximity: {
    type: String,
    required: true
  },
  news: {
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
  <div class="p-4 bg-neutral-900 flex flex-col justify-stretch items-stretch text-gray-300 border border-white rounded-2xl">
    <div class="flex flex-row justify-between items-center text-white text-lg font-medium">
      <h2>{{ name }}</h2>
      <h2>{{ location }}</h2>
    </div>
    <div class="flex flex-row justify-between items-center">
      <span>Prox. <span class="text-red-500">{{ proximity }}</span></span>
      <span>Containment: <span class="text-red-500">{{ containment }}</span></span>
      <span>Size: <span class="text-green-500">{{ size }}</span></span>
    </div>
    <div class="flex flex-row justify-between items-center gap-x-4">
      <div class="flex flex-col justify-start">
        <span>News</span>
        <p>{{ news }}</p>
      </div>
      <button class="px-4 py-2 rounded-full border border-red-500 bg-transparent hover:bg-red-500 text-red-500 hover:text-white transition-all">
        Watch
      </button>
    </div>
  </div>
</template>

