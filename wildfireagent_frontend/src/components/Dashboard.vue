<script setup>

import FireItem from "@/components/FireItem.vue";
import WatchingItem from "@/components/WatchingItem.vue";
</script>

<template>
  <div class="max-w-screen w-screen max-h-screen h-screen bg-neutral-900 p-4 flex flex-col justify-start items-stretch gap-y-4 overflow-hidden">
    <div class="border border-white text-white px-6 py-2 rounded-full text-xl">
        <input type="text" placeholder="Search..." class="bg-transparent outline-0 focus-visible:outline-none caret-white ">
    </div>
    <div class="flex-grow grid grid-rows-3 justify-stretch items-stretch gap-y-4 min-h-0">
      <div class="flex flex-col justify-start gap-y-4 items-stretch row-span-2 relative">
        <span class="text-gray-300">Nearby:</span>
        <div class="flex flex-col justify-start gap-y-4 items-stretch overflow-y-auto scroll-fade">
          <FireItem id="1" news="The fire has spread throughout the city" proximity="13mi" size="10k acres" containment="0%" location="San Bernandino" name="Line fire" />
          <FireItem id="1" news="The fire has spread throughout the city" proximity="13mi" size="10k acres" containment="0%" location="San Bernandino" name="Line fire" />
          <FireItem id="1" news="The fire has spread throughout the city" proximity="13mi" size="10k acres" containment="0%" location="San Bernandino" name="Line fire" />
          <FireItem id="1" news="The fire has spread throughout the city" proximity="13mi" size="10k acres" containment="0%" location="San Bernandino" name="Line fire" />
          <FireItem id="1" news="The fire has spread throughout the city" proximity="13mi" size="10k acres" containment="0%" location="San Bernandino" name="Line fire" />
          <FireItem id="1" news="The fire has spread throughout the city" proximity="13mi" size="10k acres" containment="0%" location="San Bernandino" name="Line fire" />
          <FireItem id="1" news="The fire has spread throughout the city" proximity="13mi" size="10k acres" containment="0%" location="San Bernandino" name="Line fire" />
        </div>

      </div>
      <div class="flex flex-col justify-start gap-y-4 items-stretch">
        <span class="text-gray-300">Watching:</span>
        <div class="flex flex-col justify-start gap-y-4 items-stretch overflow-y-auto">
          <WatchingItem id="1" name="Line Fire" bg="bg-red-500"/>
          <WatchingItem id="1" name="Airport Fire" bg="bg-green-500"/>
          <WatchingItem id="1" name="Airport Fire" bg="bg-green-500"/>
          <WatchingItem id="1" name="Airport Fire" bg="bg-green-500"/>
          <WatchingItem id="1" name="Airport Fire" bg="bg-green-500"/>
          <WatchingItem id="1" name="Airport Fire" bg="bg-green-500"/>
          <WatchingItem id="1" name="Airport Fire2" bg="bg-green-500"/>
        </div>
      </div>
    </div>


  </div>

</template>

<style scoped>
.scroll-fade {
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: auto;
  color: white;
  box-sizing: border-box;
}

.scroll-fade:after {
      content: '';
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      width:100vw;
      height: 30px;
      background: linear-gradient(to bottom, rgba(23,23,23,0),  rgba(23,23,23,1));
      pointer-events: none; /* Ensures the gradient doesn't interfere with scrolling */
}
</style>