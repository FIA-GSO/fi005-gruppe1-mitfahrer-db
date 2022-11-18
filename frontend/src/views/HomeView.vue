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
        class="text-white mt-4 text-center sm:text-left sm:mt-8 text-xl font-semibold mb-1 ml-1"
      >
        Reservierte Fahrten
      </h1>
      <RideResults :rides="data.reservedRides" />
      <div class="flex justify-center">
        <RouterLink
          :to="{ name: 'searchRides' }"
          class="block bg-white rounded px-5 py-1 mt-1 text-center font-semibold hover:bg-blue-50 hover:text-cyan-800"
        >
          Fahrt suchen
        </RouterLink>
      </div>
    </div>
    <div class="mb-8">
      <h1
        class="text-white mt-4 text-center sm:text-left sm:mt-8 text-xl font-semibold mb-1 ml-1"
      >
        Angebotene Fahrten
      </h1>
      <RideResults :rides="data.postedRides"/>
      <div class="flex justify-center">
        <RouterLink
          :to="{ name: 'createRide' }"
          class="block bg-white rounded px-5 py-1 mt-1 text-center font-semibold hover:bg-blue-50 hover:text-cyan-800"
        >
          Neue Fahrt anbieten
        </RouterLink>
      </div>
    </div>
  </main>
</template>
