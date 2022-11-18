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

async function cancelRide(id: string) {
  try {
    const response = await API(
      "rides/cancel",
      "POST",
      JSON.stringify({
        id,
      })
    );
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
    data.ride = (await response.json()).ride;
    return data.ride;
  } catch (error: any) {
    console.log(error);
  }
}

async function reserveRide(id: string) {
  try {
    const response = await fetch("http://127.0.0.1:5000/rides/reserve", {
      method: "POST",
      credentials: "include",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        id,
      }),
    }).then((r) => {
      if (!r.ok) {
        throw new Error();
      }
      return r.json();
    });
    console.log("Reserve Response", response);
    data.ride = response.ride;
  } catch (e) {}
}

async function cancelReservation(id: string) {
  try {
    const response = await fetch(
      "http://127.0.0.1:5000/rides/cancel-reservation",
      {
        method: "POST",
        credentials: "include",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          id,
        }),
      }
    ).then((r) => {
      if (!r.ok) {
        throw new Error();
      }
      return r.json();
    });
    console.log("Cancel Reservation Response", response);
    data.ride = response.ride;
  } catch (e) {}
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
    zoom: 17,
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

    map.fitBounds([coordinates, gsoLngLat], { padding: 200 });
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
    const response = await API(
      "rides/report-delay",
      "POST",
      JSON.stringify({
        id: route.params.id,
        delayMinutes,
      })
    ).then((r) => r.json());
    console.log("Delay response", response);
    data.ride = response.ride;
  } catch (error: any) {}
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
            <span class="font-semibold">Abfahrtszeit: </span>
            <span class="font-bold">{{
              new Date(data.ride.departureDateTime).toLocaleString("de-DE")
            }}</span>
          </p>
          <p class="mb-2">
            <span class="font-semibold">Ort: </span><br />
            <span
              v-for="(line, i) in addressLines"
              :class="{ 'font-bold': i === 0 }"
              >{{ line }}<br
            /></span>
          </p>
          <p class="mb-2">
            <span class="font-semibold">Kilometerpauschale: </span
            ><span class="font-bold"
              >{{ data.ride.pricePerKilometer }} € / km</span
            >
          </p>
          <!-- <p>Geschlecht: N/A</p> -->
          <p class="mb-2">
            <span class="font-semibold">Anzahl freier Sitzplätze: </span
            ><span class="font-bold">{{ data.ride.remainingSeats }}</span>
          </p>
          <p class="mb-2">
            <span class="font-semibold">Richtung: </span>
            <span class="font-bold">{{
              data.ride.direction === "to" ? "Hinfahrt" : "Rückfahrt"
            }}</span>
          </p>
          <p class="mb-2">
            <span class="font-semibold">Reserviert: </span
            ><span class="font-bold">{{
              data.ride.isReserved ? "Ja" : "Nein"
            }}</span>
          </p>
          <p class="mb-2">
            <span class="font-semibold">Verspätung: </span
            ><span class="font-bold">{{ data.ride.delayMinutes }} Minuten</span>
          </p>
          <p class="mb-2">
            <span class="font-semibold">Kontakt: </span
            ><span
              ><a
                class="font-bold underline"
                :href="'mailto:' + data.ride.contactEmail"
                >{{ data.ride.contactEmail }}</a
              ></span
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
            type="radio"
            label="Zahlungsmethode"
            name="paymentMethod"
            :options="{
              cash: 'Barzahlung',
              paypal: 'PayPal',
            }"
            option-class="!opacity-100"
            :disabled="true"
            :value="data.ride.paymentMethod"
          />
        </div>
      </div>
      <div id="map" class="grow h-96 md:h-auto" />
    </div>
    <div class="flex flex-row gap-2">
      <template v-if="!data.ride.isOwner">
        <button
          v-if="!data.ride.isReserved"
          @click="reserveRide(data.ride.id)"
          class="bg-gso-blue px-4 py-2 text-white rounded-full"
        >
          Reservieren
        </button>
        <button
          v-else
          @click="cancelReservation(data.ride.id)"
          class="bg-gso-blue px-4 py-2 text-white rounded-full"
        >
          Stornieren
        </button>
      </template>
      <template v-else>
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
