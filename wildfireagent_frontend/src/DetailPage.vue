<script setup>
import Detail from "@/components/Detail.vue";

defineProps({
  id: {
    type: String,
    required: true
  },
})
</script>

<template>
  <main>
    <Detail :id="id" />
  </main>
</template>


