<script setup>

import FireItem from "@/components/FireItem.vue";
import WatchingItem from "@/components/WatchingItem.vue";
</script>

<template>
  <div class="max-w-screen w-screen max-h-screen h-screen bg-neutral-900 p-4 flex flex-col justify-between items-stretch">
    <div class="flex flex-col justify-start gap-y-4 items-stretch">
      <div class="border border-white text-white px-6 py-2 rounded-full text-xl">
        <input type="text" placeholder="Search..." class="bg-transparent outline-0 focus-visible:outline-none caret-white ">
      </div>
      <span class="text-gray-300">Nearby:</span>
      <FireItem id="1" news="The fire has spread throughout the city" proximity="13mi" size="10k acres" containment="0%" location="San Bernandino" name="Line fire" />
      <FireItem id="1" news="The fire has spread throughout the city" proximity="13mi" size="10k acres" containment="0%" location="San Bernandino" name="Line fire" />
    </div>
    <div class="flex flex-col justify-start gap-y-4 items-stretch">
      <div class="flex flex-col justify-start gap-y-4 items-stretch">
        <span class="text-gray-300">Watching:</span>
        <WatchingItem id="1" name="Line Fire" bg="bg-red-500"/>
        <WatchingItem id="1" name="Airport Fire" bg="bg-green-500"/>
      </div>

    </div>

  </div>

</template>

<style scoped>

</style>