<script setup lang="ts">
import RideListing from "@/components/RideListing.vue";
import RideResults from "@/components/RideResults.vue";
import { API } from "@/utils/utils";
import { onMounted, reactive } from "vue";

interface HomeData {
  postedRides: [any];
  reservedRides: [any];
}

const data = reactive({
  postedRides: [],
  reservedRides: [],
});

async function getPostedRides() {
  const response = await API("rides/posted");
  console.log("posted rides response", response);
  data.postedRides = response.data.rides;
}

async function getReservedRides() {
  const response = await API("rides/reserved");
  console.log("reserved rides response", response);
  data.reservedRides = response.data.rides;
}

onMounted(() => {
  getPostedRides();
  getReservedRides();
});
</script>

<template>
  <main class="flex sm:items-center">
    <div class="grow">
      <h1
        class="text-white mt-4 text-center sm:text-left sm:mt-12 text-xl font-semibold mb-1 ml-1"
      >
        Angebotene Fahrten
      </h1>
      <RideResults :rides="data.postedRides" />
      <RouterLink
        :to="{ name: 'createRide' }"
        class="block bg-white sm:rounded p-2 py-1 w-full border-y sm:border border-black mt-1 text-center"
      >
        Fahrt anbieten
      </RouterLink>
    </div>
    <div class="mb-8">
      <h1 class="text-white mt-8 sm:mt-12 text-xl font-semibold mb-1 ml-1">
        Reservierte Fahrten
      </h1>
      <RideResults :rides="data.reservedRides" />
      <RouterLink
        :to="{ name: 'searchRides' }"
        class="block bg-white sm:rounded p-2 py-1 w-full border-y sm:border border-black mt-1 text-center"
      >
        Neue Fahrt suchen
      </RouterLink>
    </div>
  </main>
</template>
