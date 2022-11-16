<script setup lang="ts">
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";
import { onMounted, reactive } from "vue";
import { useRoute } from "vue-router";
const route = useRoute();

interface DetailData {
  ride: any | null;
}

const data: DetailData = reactive({
  ride: null,
});

async function getRide(id: string): Promise<any> {
  const response = await fetch(
    "http://127.0.0.1:5000/rides/detail?" + new URLSearchParams({ id }),
    {
      method: "GET",
      credentials: "include",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    }
  ).then((r) => {
    if (!r.ok) {
      throw new Error();
    }
    return r.json();
  });
  console.log("ride detail response", response);
  data.ride = response.ride;
  return response.ride;
}

async function createMap(coordinates: any) {
  console.log("Map loaded", coordinates);
  mapboxgl.accessToken =
    "pk.eyJ1IjoiZ3NvbWl0ZmFocmVyZGIiLCJhIjoiY2xhaThmaGw3MDA3cjN2cGdvcXoyaGJjNyJ9.njwSq8e35577L6DyujSyKQ";
  const map = new mapboxgl.Map({
    container: "map",
    style: "mapbox://styles/mapbox/light-v9",
    center: coordinates,
    zoom: 15,
  });
  const marker = new mapboxgl.Marker().setLngLat(coordinates).addTo(map);
  map.on("load", () => {
    // TODO: Here we want to load a layer
    // TODO: Here we want to load/setup the popup
  });
}

const isMounted = new Promise<void>((resolve) => onMounted(resolve));

async function setup() {
  const rideId = route.params.id as string;
  const ride = await getRide(rideId);
  await isMounted;
  createMap([
    ride.departureCoordinates.longitude,
    ride.departureCoordinates.latitude,
  ]);
}

setup();
</script>

<template>
  <main class="bg-white p-8 grid grid-cols-2">
    <div>
      <div v-if="data.ride">
        <p>
          Abfahrtszeit:
          {{ new Date(data.ride.departureDateTime).toLocaleString("de-DE") }}
        </p>
        <p>Ort: {{ data.ride.address }}</p>
        <p>Kilometerpauschale: {{ data.ride.pricePerKilometer }}</p>
        <!-- <p>Geschlecht: N/A</p> -->
        <p>Anzahl freier Sitzplätze: {{ data.ride.remainingSeats }}</p>
        <p>Richtung: {{ data.ride.direction }}</p>
      </div>
    </div>
    <div id="map" />
  </main>
</template>
