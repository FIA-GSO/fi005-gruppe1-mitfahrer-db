<script setup lang="ts">
import { computed } from "@vue/reactivity";

const props = defineProps({
  ride: {
    type: Object as any,
  },
});
const flip = computed(() => {
  return props.ride?.direction === "from";
});
const addressLines = (address: string) => {
  return address.split(", ");
};
</script>

<template>
  <div
    class="text-xs px-3 p-2 flex flex-row justify-between items-center hover:bg-blue-50 hover:text-cyan-800 cursor-pointer border-b"
    :class="{ 'opacity-30': ride.isExpired }"
  >
    <div
      class="route grid grid-cols-[40%_min-content_40%] sm:grid-cols-[30%_min-content_30%_1fr] gap-4 items-center w-full"
    >
      <div
        :class="{
          'order-1': flip,
          'order-4': !flip,
        }"
        class="text-center flex flex-col"
      >
        <span class="text-xl font-bold text-center">GSO</span>
        <span class="text-xs text-center">Westerwaldstraße 92</span>
        <span class="text-xs text-center">51105 Köln</span>
      </div>
      <font-awesome-icon
        icon="fa-solid fa-arrow-right"
        class="px-2 text-lg"
        :class="{ 'order-2': flip, 'order-3': !flip }"
      />
      <div
        class="font-semibold text-center"
        :class="{ 'order-3': flip, 'order-2': !flip }"
      >
        <div
          v-for="(line, i) in addressLines(props.ride.address)"
          class="whitespace-nowrap"
          :class="{ 'font-bold': i === 0 }"
        >
          {{ line }}
        </div>
      </div>
      <div class="order-4 text-sm text-center flex flex-col hidden sm:flex">
        <span class="time" :class="{}">
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
        <span v-if="props.ride.delayMinutes" class="text-red-600"
          >+ {{ props.ride.delayMinutes }}</span
        >
        <span v-if="props.ride.distance != null">
          {{ (props.ride.distance / 1000).toFixed(2) }} km
        </span>
        <div class="flex items-center justify-center">
          <img
            v-if="props.ride.userImage"
            class="w-8 h-8 rounded-full overflow-hidden"
            :src="'http://127.0.0.1:5000/' + props.ride.userImage"
          />
        </div>
      </div>
    </div>
  </div>
</template>

Kann und Muss Kriterien, Spalte Erfuellt, Spalte Bemerkungen
