<script setup lang="ts">
import RideListing from "@/components/RideListing.vue";
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
  const response = await fetch("http://127.0.0.1:5000/rides/posted", {
    method: "GET",
    credentials: "include",
  }).then((r) => {
    if (!r.ok) {
      throw new Error("Fail");
    }
    return r.json();
  });
  console.log("posted rides response", response);
  data.postedRides = response.rides;
}

async function getReservedRides() {
  const response = await fetch("http://127.0.0.1:5000/rides/reserved", {
    method: "GET",
    credentials: "include",
  }).then((r) => {
    if (!r.ok) {
      throw new Error("Fail");
    }
    return r.json();
  });
  console.log("reserved rides response", response);
  data.reservedRides = response.rides;
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
          :to="{name: 'rideDetails', params: {id: ride.id}}"
        >
          <RideListing :ride="ride" />
        </RouterLink>
      </div>
      <RouterLink
        :to="{name: 'createRide'}"
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
        <RideListing v-for="ride in data.reservedRides" :ride="ride" />
      </div>
      <RouterLink
        :to="{name: 'searchRides'}"
        class="block bg-white rounded p-2 py-1 w-full border border-black mt-1 text-center"
      >
        Neue Fahrt suchen
      </RouterLink>
    </div>
  </main>
</template>
