<script setup lang="ts">
import RideListing from "@/components/RideListing.vue";
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
  const response = await API("rides/posted")
  console.log("posted rides response", response);
  data.postedRides = (await response.json()).rides;
}

async function getReservedRides() {
  const response = await API("rides/reserved")
  console.log("reserved rides response", response);
  data.reservedRides = (await response.json()).rides;
}

onMounted(() => {
  getPostedRides();
  getReservedRides();
});
</script>

<template>
  <main class="flex items-center">
    <div>
      <h1 class="text-white mt-12 text-xl font-semibold mb-1 ml-1">
        Angebotene Fahrten
      </h1>
      <div class="bg-white w-[600px] rounded-md overflow-hidden">
        <RouterLink
          v-for="(ride, i) in data.postedRides"
          :to="{ name: 'rideDetails', params: { id: ride.id } }"
        >
          <RideListing :ride="ride" />
        </RouterLink>
      </div>
      <RouterLink
        :to="{ name: 'createRide' }"
        class="block bg-white rounded p-2 py-1 w-full border border-black mt-1 text-center"
      >
        Fahrt anbieten
      </RouterLink>
    </div>
    <div>
      <h1 class="text-white mt-12 text-xl font-semibold mb-1 ml-1">
        Reservierte Fahrten
      </h1>
      <div class="bg-white w-[600px] rounded-md overflow-hidden">
        <RouterLink
          v-for="ride in data.reservedRides"
          :to="{ name: 'rideDetails', params: { id: ride.id } }"
        >
          <RideListing :ride="ride" />
        </RouterLink>
      </div>
      <RouterLink
        :to="{ name: 'searchRides' }"
        class="block bg-white rounded p-2 py-1 w-full border border-black mt-1 text-center"
      >
        Neue Fahrt suchen
      </RouterLink>
    </div>
  </main>
</template>
