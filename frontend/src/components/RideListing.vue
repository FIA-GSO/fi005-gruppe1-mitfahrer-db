<script setup lang="ts">
const props = defineProps({
  ride: {
    type: Object as any,
  },
});
const addressLines = (address: string) => {
  return address.split(", ");
};
</script>

<template>
  <div
    class="text-xs px-3 p-2 flex flex-row justify-between items-center hover:bg-blue-50 hover:text-cyan-800 cursor-pointer border-b"
  >
    <div class="route flex flex-row gap-8">
      <div class="font-semibold w-[155px]">
        <div
          v-for="(line, i) in addressLines(props.ride.departureAddress)"
          :class="{ 'font-bold': i === 0 }"
        >
          {{ line }}
        </div>
      </div>
      <div class="flex items-center justify-center">
        <font-awesome-icon icon="fa-solid fa-car-side" class="px-2 text-lg" />
      </div>
      <div class="font-semibold w-[150px]">
        <div
          v-for="(line, i) in addressLines(props.ride.arrivalAddress)"
          :class="{ 'font-bold': i === 0 }"
        >
          {{ line }}
        </div>
      </div>
    </div>
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
