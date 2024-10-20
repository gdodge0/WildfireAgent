<script setup>
import { ref, onMounted } from 'vue';
import FireItem from "@/components/FireItem.vue";
import WatchingItem from "@/components/WatchingItem.vue";
import {fetchFireItems, fetchBatchLatestNews} from "@/utils/api.js";
import getNClosestLocations from "@/utils/location.js";
import promptUserLocation from "@/utils/browser.js";
import deepSearchObject from "@/utils/search.js";

let totalFires = [];
let matchingFires = [];
let searchTerm = ref();
let fireItems = ref([]);
let show_nearby = true
let closest_3_fires = []
const error = ref(null);
let headline_debounce_timout;

function debounceRefreshHeadlines() {
    clearTimeout(headline_debounce_timout);
    headline_debounce_timout = setTimeout(() => refreshHeadlines(), 1000); // 300ms debounce
}

async function refreshHeadlines(){
  console.log("getting headlines")
  const news = await fetchBatchLatestNews(fireItems.value)
  news.forEach((headline) => {
    const fire = fireItems.value.find(fire => String(fire.id) === String(headline["id"]));
    fire.news = headline["headline"]
    fire.news_timestamp = headline["time"]
  })


}

// this is called when promptUserLocation successfully returns
async function gatherNearbyFires(userLocation) {
  closest_3_fires = getNClosestLocations(totalFires, userLocation)
  closest_3_fires.forEach((fire) => {
    fireItems.value.push(fire)
  })
  refreshHeadlines()
}

function performSearch() {
  show_nearby = searchTerm.value === ""
  const searchTermLower = String(searchTerm.value).toLowerCase();  // Convert search term to lowercase

  // Deep search through all fire objects
  matchingFires = totalFires.filter(fire => {
      return deepSearchObject(fire, searchTermLower);
  });

  fireItems.value = []
  if (show_nearby)
  {
    closest_3_fires.forEach((fire) => {
      fireItems.value.push(fire)
    })
  } else {
    matchingFires.forEach((fire) => {
      fireItems.value.push(fire)
    })
  }

  debounceRefreshHeadlines()
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
</script>

<template>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&icon_names=location_on" />
  <div class="max-w-screen w-screen max-h-screen h-screen bg-neutral-900 p-4 flex flex-col justify-start items-stretch gap-y-4 overflow-hidden">
    <div class="border border-white text-white px-6 py-2 rounded-full text-xl">
        <input
          id="searchbar"
          type="text"
          placeholder="Search..."
          class="bg-transparent outline-0 focus-visible:outline-none caret-white"
          v-model="searchTerm"
          @input="performSearch(searchTerm, totalFires)"
        />
    </div>
    <div class="flex-grow grid grid-rows-3 justify-stretch items-stretch gap-y-4 min-h-0">
      <div class="flex flex-col justify-start gap-y-4 items-stretch row-span-3 relative">
        <span class="text-gray-300">
          <template v-if="show_nearby">
            Nearby:
          </template>
          <template v-else>
            Found {{ matchingFires.length }} matching fires
          </template>
        </span>
        <div class="flex flex-col justify-start gap-y-4 items-stretch overflow-y-auto scroll-fade">
          <FireItem
            v-for="(fire, index) in fireItems"
            :key="index"
            :id="fire.id"
            :news="fire.news"
            :news_timestamp="fire.news_timestamp"
            :proximity="fire.proximity"
            :size="fire.data.acreage"
            :containment="fire.data.containment"
            :location="fire.address"
            :name="fire.name"
          />
        </div>

      </div>
      <div class="hidden flex-col justify-start gap-y-4 items-stretch">
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