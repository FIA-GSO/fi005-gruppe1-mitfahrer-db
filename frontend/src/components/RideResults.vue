<script setup lang="ts">
import RideListing from "@/components/RideListing.vue";
defineProps({
  rides: {
    type: Object as () => [any],
  },
});
</script>

<template>
  <div class="bg-white rounded-md overflow-hidden">
    <RouterLink
      v-for="ride in rides"
      :to="{ name: 'rideDetails', params: { id: ride.id } }"
    >
      <RideListing :ride="ride" />
    </RouterLink>
  </div>
</template>
