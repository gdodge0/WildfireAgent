<script setup>
import { GoogleMap, CustomMarker } from 'vue3-google-map'
import { getCurrentInstance, reactive, ref, onMounted } from 'vue'

// Access global properties using getCurrentInstance()
const instance = getCurrentInstance()
const gmaps_api_key = instance.appContext.config.globalProperties.$gmaps_api_key



// Props: fireCoordinates input (array of fire locations)
defineProps({
  fireCoordinates: {
    type: Array,
    required: true,
    default: () => [  ]
  }
})


// Define the custom SVG ico

</script>

<template>
  <GoogleMap
      :api-key="gmaps_api_key"
      style="width: 100%; height: 100%"
      :center="fireCoordinates[0]"
      :zoom="12"
  >
    <!-- Loop through fire coordinates and add a marker for each location -->
    <CustomMarker v-for="(fire, index) in fireCoordinates"
                  :options="{ position: fire, anchorPoint: 'BOTTOM_CENTER' }">
      <img alt="fire icon" src="./icons/flame-icon.svg" width="50" height="50" />

    </CustomMarker>
  </GoogleMap>
</template>

<style scoped>

</style>
