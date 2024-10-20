<script setup>
import { ref, onMounted } from 'vue';
import FireItem from "@/components/FireItem.vue";
import WatchingItem from "@/components/WatchingItem.vue";
import {fetchFireItems, fetchBatchLatestNews} from "@/utils/api.js";
import getNClosestLocations from "@/utils/location.js";
import promptUserLocation from "@/utils/browser.js";

let totalFires = [];
let fireItems = ref([]);
const error = ref(null);

// this is called when promptUserLocation successfully returns
async function gatherNearbyFires(userLocation) {
  let locations = getNClosestLocations(totalFires, userLocation)
  locations.forEach((fire) => {
    fireItems.value.push(fire)
  })

  const news = await fetchBatchLatestNews(locations)
  console.log(news)
  news.forEach((headline) => {
    const fire = fireItems.value.find(fire => String(fire.id) === String(headline["id"]));
    fire.news = headline["headline"]
  })
}

// Fetch the data when the component is mounted
onMounted(async () => {
  totalFires = await fetchFireItems();
  promptUserLocation(gatherNearbyFires);
});

// Watching Items state
const watchingItems = ref([
  { id: `33389`, name: "Line Fire", bg: "bg-red-500" },
  { id: `33685`, name: "Bridge Fire", bg: "bg-green-500" }
]);

// Function to add a new Watching Item
const addWatchingItem = () => {
  const newWatchingItem = {
    id: `33389`,
    name: "New Watch Fire",
    bg: "bg-blue-500"
  };
  watchingItems.value.push(newWatchingItem);
};
</script>

<template>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&icon_names=location_on" />
  <div class="max-w-screen w-screen max-h-screen h-screen bg-neutral-900 p-4 flex flex-col justify-start items-stretch gap-y-4 overflow-hidden">
    <div class="border border-white text-white px-6 py-2 rounded-full text-xl">
        <input type="text" placeholder="Search..." class="bg-transparent outline-0 focus-visible:outline-none caret-white ">
    </div>
    <div class="flex-grow grid grid-rows-3 justify-stretch items-stretch gap-y-4 min-h-0">
      <div class="flex flex-col justify-start gap-y-4 items-stretch row-span-2 relative">
        <span class="text-gray-300">Nearby:</span>
        <div class="flex flex-col justify-start gap-y-4 items-stretch overflow-y-auto scroll-fade">
          <FireItem
            v-for="(fire, index) in fireItems"
            :key="index"
            :id="fire.id"
            :news="fire.news"
            :proximity="fire.proximity"
            :size="fire.data.acreage"
            :containment="fire.data.containment"
            :location="fire.address"
            :name="fire.name"
          />
        </div>

      </div>
      <div class="flex flex-col justify-start gap-y-4 items-stretch">
        <span class="text-gray-300">Watching:</span>
        <div class="flex flex-col justify-start gap-y-4 items-stretch overflow-y-auto">
          <WatchingItem
            v-for="(watch, index) in watchingItems"
            :key="index"
            :id="watch.id"
            :name="watch.name"
            :bg="watch.bg"
          />
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