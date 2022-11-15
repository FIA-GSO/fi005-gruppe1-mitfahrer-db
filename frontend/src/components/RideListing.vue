<script setup lang="ts">
const props = defineProps({
  ride: {
    type: Object as any,
  },
});
</script>

<template>
  <div class="text-lg px-3 p-2 flex flex-row justify-between items-center">
    <span class="route">
      <span class="font-semibold">{{ props.ride.departureAddress }}</span>
      <font-awesome-icon icon="fa-solid fa-car-side" class="px-2" />
      <span class="font-semibold">{{ props.ride.arrivalAddress }}</span>
    </span>
    <span class="time text-base">
      {{
        new Date(props.ride.departureDateTime).toLocaleString("de-DE", {
          day: "2-digit",
          month: "2-digit",
          year: "numeric",
          hour: "2-digit",
          minute: "2-digit",
        })
      }}
    </span>
  </div>
</template>
