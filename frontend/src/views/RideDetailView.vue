<script setup lang="ts">
import { API } from "@/utils/utils";
import { computed } from "@vue/reactivity";
import { propsToAttrMap } from "@vue/shared";
import mapboxgl, { type LngLatLike } from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";
import { onMounted, reactive } from "vue";
import { useRoute, useRouter } from "vue-router";
const route = useRoute();
const router = useRouter();

interface DetailData {
  ride: any | null;
}

const data: DetailData = reactive({
  ride: null,
});

async function startRide(id: string) {
  const locations = data.ride.reservations.map((r) => r.location);
  const lines = ["Abholorte der Reservierungen:", ...locations];
  alert(lines.join("\n"));
  const response = await API("rides/start", "POST", {
    id,
  });
  data.ride = response.data.ride;
}

async function cancelRide(id: string) {
  try {
    const response = await API("rides/cancel", "POST", {
      id,
    });
    console.log(response);
    router.push({
      path: "/",
    });
  } catch (e) {
    console.log(e);
  }
}

async function getRide(id: string): Promise<any> {
  try {
    console.log("ID", id);
    const response = await API(`rides/detail?id=${id}`);
    console.log("ride detail response", response);
    data.ride = response.data.ride;
    return data.ride;
  } catch (error: any) {
    console.log(error);
  }
}

async function reserveRide(id: string) {
  try {
    const input = prompt("Bitte geben Sie einen Abholort ein");
    if (input) {
      const response = await API("rides/reserve", "POST", {
        id,
        location: input,
      });
      console.log("Reserve Response", response);
      data.ride = response.data.ride;
    }
  } catch (e) {}
}

async function cancelReservation(id: string) {
  try {
    const response = await API("rides/cancel-reservation", "POST", { id });
    console.log("Cancel Reservation Response", response);
    data.ride = response.data.ride;
  } catch (e) {
    console.log(e);
  }
}

async function createMap(coordinates: LngLatLike, direction: string) {
  console.log("Map loaded", coordinates);
  mapboxgl.accessToken =
    "pk.eyJ1IjoiZ3NvbWl0ZmFocmVyZGIiLCJhIjoiY2xhaThmaGw3MDA3cjN2cGdvcXoyaGJjNyJ9.njwSq8e35577L6DyujSyKQ";

  const gsoLngLat: LngLatLike = [6.995640957065214, 50.927547849999996];

  const map = new mapboxgl.Map({
    container: "map",
    style: "mapbox://styles/mapbox/light-v9",
    center: direction == "to" ? coordinates : gsoLngLat,
    zoom: 20,
  });

  map.on("load", () => {
    new mapboxgl.Marker({
      color: direction == "from" ? "#5bd56d" : "#85b5cc",
    })
      .setLngLat(coordinates)
      .setPopup(
        new mapboxgl.Popup({ closeButton: false }).setHTML(
          `<h1>${direction === "from" ? "Ankunft" : "Abfahrt"}</h1>`
        )
      )
      .addTo(map);

    new mapboxgl.Marker({
      color: direction == "to" ? "#5bd56d" : "#85b5cc",
    })
      .setLngLat(gsoLngLat)
      .setPopup(
        new mapboxgl.Popup({ closeButton: false }).setHTML(
          `<h1>${direction === "to" ? "Ankunft" : "Abfahrt"}</h1>`
        )
      )
      .addTo(map);

    map.fitBounds([coordinates, gsoLngLat], { padding: 100 });
  });
}

const isMounted = new Promise<void>((resolve) => onMounted(resolve));

async function setup() {
  const rideId = route.params.id as string;
  const ride = await getRide(rideId);
  await isMounted;
  createMap(
    [ride.coordinates.longitude, ride.coordinates.latitude],
    ride.direction
  );
}

async function reportDelay() {
  const response = window.prompt("Abfahrtszeit aktualisieren");
  console.log("Response", response);
  if (response == null) {
    return;
  }
  const delayMinutes = parseInt(response);
  try {
    const response = await API("rides/report-delay", "POST", {
      id: route.params.id,
      delayMinutes,
    });
    console.log("Delay response", response);
    data.ride = response.data.ride;
  } catch (error: any) {
    console.log(error);
  }
}

const addressLines = computed(() => {
  return data.ride.address.split(", ");
});

setup();
</script>

<template>
  <main class="bg-white p-8">
    <div class="flex md:flex-row flex-col gap-6 mb-6">
      <div>
        <div v-if="data.ride">
          <p class="mb-2">
            <img
            v-if="data.ride.userImage"
            class="w-8 h-8 rounded-full mr-3 overflow-hidden inline"
            :src="'http://127.0.0.1:5000/' + data.ride.userImage"
          />
            <span class="font-semibold">{{data.ride.contactEmail}} 
              <font-awesome-icon v-if="data.ride.ownerGender === 'male'" icon="fa-solid fa-mars" class="text-blue-400"/>
              <font-awesome-icon v-if="data.ride.ownerGender === 'female'" icon="fa-solid fa-venus" class="text-red-400"/>
              <font-awesome-icon v-if="data.ride.ownerGender === 'other'" icon="fa-solid fa-genderless" class="text-violet-400"/>
            </span>
            
            <span v-if="data.ride.isStartet" class="font-semibold text-xs uppercasetext-orange-500">Gestartet</span>
            <span v-else class="font-semibold text-xs uppercase text-gray-500">Nicht gestartet</span>
            
          </p>
          <p class="mb-2">
            <span class="font-semibold">Abfahrt: </span>
            <span class="font-bold">{{
              new Date(data.ride.departureDateTime).toISOString().split('T')[1].slice(0, 5)
            }} Uhr </span>
            <span v-if="data.ride.delayMinutes > 0" class="font-bold text-red-500">
              + {{ data.ride.delayMinutes }} min
            </span>
          </p>
          <p class="mb-2">
            <span class="font-semibold">Von:</span><br />
            <span
            v-if="data.ride.direction === 'to'" v-for="(line, i) in addressLines"
              :class="{ 'font-bold': i === 0 }"
              >{{ line }}<br
            /></span>
            <span v-else v-for="(line, i) in ['GSO', 'Westerwaldstraße 91', '51105 Köln']"
              :class="{ 'font-bold': i === 0 }">
              <font-awesome-icon v-if="i === 0" icon="fa-solid fa-school"/> {{ line }}<br>
            </span>
          </p>
          <p class="mb-2">
            <span class="font-semibold">Nach:</span><br />
            <span
              v-if="data.ride.direction === 'from'" v-for="(line, i) in addressLines"
              :class="{ 'font-bold': i === 0 }"
              >{{ line }}<br
            /></span>
            <span v-else v-for="(line, i) in ['GSO', 'Westerwaldstraße 91', '51105 Köln']"
              :class="{ 'font-bold': i === 0 }">
              <font-awesome-icon v-if="i === 0" icon="fa-solid fa-school"/> {{ line }}<br>
            </span>
          </p>
          <p class="mb-2">
            <span class="font-semibold">Kilometerpauschale: </span
            ><span class="font-bold"
              >{{ data.ride.pricePerKilometer }} € / km</span
            >
          </p>
          <p class="mb-2">
            <span class="font-semibold">Anzahl freier Sitzplätze: </span
            ><span class="font-bold">{{ data.ride.remainingSeats }}</span>
          </p>
          <p class="mb-2">
            <a
                class="font-bold underline"
                :href="'mailto:' + data.ride.contactEmail"
                >Kontakt (E-Mail)</a
              >
          </p>
          <FormKit
            type="checkbox"
            label="Sonstiges"
            :options="{
              pets: 'Haustiere',
              smoker: 'Raucher Fahrzeug',
              coronaHygiene: 'Corona Hygiene Regeln',
            }"
            option-class="!opacity-100"
            :disabled="true"
            :value="data.ride.other"
          />
          <FormKit
            type="checkbox"
            label="Zahlungsmethoden"
            name="paymentMethod"
            :options="{
              cash: 'Barzahlung',
              paypal: 'PayPal',
            }"
            option-class="!opacity-100"
            :disabled="true"
            :value="data.ride.paymentMethods"
          />
        </div>
      </div>
      <div id="map" class="grow h-96 md:h-auto" />
    </div>
    <div class="flex flex-row gap-2" v-if="!data?.ride?.isStarted">
      <template v-if="!data?.ride?.isOwner">
        <button
          v-if="!data?.ride?.isReserved && !data?.ride?.isExpired"
          @click="reserveRide(data.ride.id)"
          class="bg-gso-blue px-4 py-2 text-white rounded-full"
        >
          Reservieren
        </button>
        <button
          v-else-if="!data.ride.isExpired"
          @click="cancelReservation(data.ride.id)"
          class="bg-gso-blue px-4 py-2 text-white rounded-full"
        >
          Reservierung Stornieren
        </button>
      </template>
      <template v-else>
        <button
          @click="startRide(data.ride.id)"
          class="bg-gso-blue px-4 py-2 text-white rounded-full"
        >
          Fahrt Starten
        </button>
        <button
          @click="cancelRide(data.ride.id)"
          class="bg-gso-blue px-4 py-2 text-white rounded-full"
        >
          Fahrt Stornieren
        </button>
        <button
          @click="reportDelay"
          class="bg-gso-blue px-4 py-2 text-white rounded-full"
        >
          Verspätung melden
        </button>
      </template>
    </div>
  </main>
</template>
