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
    class="text-xs px-3 p-2 flex flex-col-reverse sm:flex-row justify-between items-center hover:bg-blue-50 hover:text-cyan-800 cursor-pointer border-b"
    :class="{ 'opacity-30': ride.isExpired }">
    <div
      class="flex gap-4 items-center grow w-full sm:w-auto">
      <div class="font-semibold text-center basis-40 sm:w-40 grow">
        <div v-for="(line, i) in props.ride.direction == 'to' ? addressLines(props.ride.address) : ['GSO', 'Westerwaldstraße 92', '51105 Köln']" class="whitespace-nowrap"
          :class="{ 'font-bold': i === 0 }">
          {{ line }}
        </div>
      </div>
      <font-awesome-icon icon="fa-solid fa-arrow-right" class="px-2 text-lg" />
      <div class="font-semibold text-center basis-40 sm:w-40 grow">
        <div v-for="(line, i) in props.ride.direction == 'from' ? addressLines(props.ride.address) : ['GSO', 'Westerwaldstraße 92', '51105 Köln']" class="whitespace-nowrap"
          :class="{ 'font-bold': i === 0 }">
          {{ line }}
        </div>
      </div>

    </div>
    <div class="flex gap-4 ml-8 flex-row-reverse sm:flex-row align-start w-full sm:w-auto">
      <div class="text-sm grow text-left sm:text-center flex flex-row sm:flex-col gap-4 sm:gap-0 sm:flex items-center">
        <span class="time">
          {{
              new Date(props.ride.departureDateTime).toLocaleString("de-DE", {
                day: "2-digit",
                month: "2-digit",
                year: "numeric",
              })
          }}
        </span>

        <span>{{
            new Date(props.ride.departureDateTime).toLocaleString("de-DE", {
              hour: "2-digit",
              minute: "2-digit"
            })
        }} <span v-if="props.ride.delayMinutes" class="text-red-600">+ {{ props.ride.delayMinutes }}</span></span>

        <span v-if="props.ride.distance != null">
          {{ (props.ride.distance / 1000).toFixed(2) }} km
        </span>

        

      </div>
      <div class="flex items-center justify-center">
          <img
            v-if="props.ride.userImage"
            class="w-8 h-8 rounded-full overflow-hidden"
            :src="'http://127.0.0.1:5000/' + props.ride.userImage"
          />
        </div>
    </div>
  </div>
</template>

Kann und Muss Kriterien, Spalte Erfuellt, Spalte Bemerkungen
