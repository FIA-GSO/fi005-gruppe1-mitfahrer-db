<script setup lang="ts">
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
onMounted(() => {
  getPostedRides();
});
</script>

<template>
  <main>
    <div class="bg-white">
      <pre v-for="ride in data.rides">{{ JSON.stringify(ride, null, 2) }}</pre>
    </div>
  </main>
</template>
