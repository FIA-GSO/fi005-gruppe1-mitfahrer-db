<script setup lang="ts">
import RideListing from "@/components/RideListing.vue";
import { onMounted, reactive } from "vue";

const data = reactive({
  rides: [],
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
  data.rides = response.rides;
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
  data.rides = response.rides;
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
      <div class="bg-white w-96 rounded-md h-40">
        <RideListing v-for="ride in data.rides" :ride="ride" />
        <!-- <pre v-for="ride in data.rides">{{ JSON.stringify(ride, null, 2) }}</pre> -->
      </div>
      <button class="bg-white rounded p-2 py-1 w-full border border-black mt-1">
        Neue Fahrt anbieten
      </button>
    </div>
    <div>
      <h1 class="text-white mt-12 text-xl font-semibold mb-1 ml-1">
        Reservierte Fahrten
      </h1>
      <div class="bg-white w-96 rounded-md h-40">
        <RideListing v-for="ride in data.rides" :ride="ride" />
        <!-- <pre v-for="ride in data.rides">{{ JSON.stringify(ride, null, 2) }}</pre> -->
      </div>
      <button class="bg-white rounded p-2 py-1 w-full border border-black mt-1">
        Neue Fahrt suchen
      </button>
    </div>
  </main>
</template>
