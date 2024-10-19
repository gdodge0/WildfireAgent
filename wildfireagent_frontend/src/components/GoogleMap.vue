<script setup>
import { GoogleMap, Marker } from 'vue3-google-map'
import { getCurrentInstance } from 'vue'

// Access global properties using getCurrentInstance()
const instance = getCurrentInstance()
const gmaps_api_key = instance.appContext.config.globalProperties.$gmaps_api_key

const center = { lat: 37.784336, lng: -122.4059412 }
</script>

<template>
  <GoogleMap
    :api-key="gmaps_api_key"
    style="width: 80%; height: 500px"
    :center="center"
    :zoom="15"
  >
    <Marker :options="{ position: center }" />
  </GoogleMap>
</template>


<style scoped>
.map-container {
  display: flex;
  justify-content: center;
}
</style>