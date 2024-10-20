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
    type: Number,
    required: true
  },
  size: {
    type: Number,
    required: true
  },
  proximity: {
    type: Number,
    required: true
  },
  news: {
    type: String,
    required: true
  },
  news_timestamp: {
    type: String,
    required: true,
    default: "Loading..."
  },
  id: {
    type: String,
    required: true
  },

})
</script>

<template>
  <div class="p-4 bg-neutral-900 flex flex-col justify-stretch items-stretch text-gray-300 border border-white rounded-2xl">
    <div class="flex flex-row justify-between items-start text-white text-lg font-medium">
      <div>
        <h2 class="line-clamp-1">{{ name }}</h2>
        <div class="flex flex-row justify-between items-center text-gray-500 text-sm">
          <h2>{{ Math.floor(proximity) }} miles away</h2>
        </div>
      </div>
      <router-link :to="{ path: '/detail/' + id }" class="px-4 py-2 line-clamp-1 rounded-full border border-red-500 bg-transparent hover:bg-red-500 text-red-500 hover:text-white font-medium transition-all">
        View 🔥
      </router-link>
    </div>

    <div class="mt-2 flex flex-row justify-start align-middle items-center text-white text-sm font-medium">
      <span class="material-symbols-outlined mr-1">location_on</span><h2>{{ location }}</h2>
    </div>
    <div class="mt-2"></div>
    <div class="flex flex-row justify-between items-center">
      <span>Containment: <span class="text-red-500">{{ containment === null ? "Unknown" : containment + "%" }}</span></span>
      <span>Size: <span class="text-green-500">{{ size === null ? "Unknown" : size + " acres"}}</span></span>
    </div>
    <div class="flex flex-row justify-between items-center gap-x-4">
      <div class="flex flex-row items-center justify-start">
        <span>Latest Info:</span><span class="ml-2 text-gray-500 text-sm">{{ news_timestamp }}</span>
        </div>
    </div>
    <p class="line-clamp-3 ">{{ news }}</p>
  </div>
</template>

