<script setup>
import HelloWorld from './components/HelloWorld.vue'
import TheWelcome from './components/TheWelcome.vue'
import FireItem from "@/components/FireItem.vue";
</script>

<template>
  <header>
    <img alt="Vue logo" class="logo" src="./assets/logo.svg" width="125" height="125" />
    <span class="text-red-500 font-medium">tester</span>
    <div class="wrapper">
      <HelloWorld msg="You did it!" />
    </div>
  </header>

  <main>
    <div class="bg-neutral-900 p-4">
      <FireItem id="1" news="The fire has spread throughout the city" proximity="13mi" size="10k acres" containment="0%" location="San Bernandino" name="Line fire" />
    </div>
  </main>
</template>


