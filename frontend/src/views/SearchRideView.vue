<script setup lang="ts">
import RideListing from "@/components/RideListing.vue";
import { reactive } from "vue";
import { useRouter } from "vue-router";
const router = useRouter();

const data = reactive({
  rides: [],
});

async function submit(formData: any) {
  const response = await fetch(
    "http://127.0.0.1:5000/rides/search?" + new URLSearchParams(formData),
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
  data.rides = response.rides;
  console.log("search rides response", response);
}
</script>

<template>
  <main class="bg-white p-8">
    <div>
      <FormKit type="form" submit-label="Fahrt suchen" @submit="submit">
        <div class="flex flex-col md:flex-row w-auto md:gap-8">
          <div class="grow">
            <FormKit type="date" name="date" label="Abfahrtsdatum" />
            <div class="flex flex-row w-full gap-4">
              <FormKit
                type="time"
                name="timeRangeStart"
                label="Von"
                outer-class="grow"
              />
              <FormKit
                type="time"
                name="timeRangeEnd"
                label="Bis"
                outer-class="grow"
              />
            </div>
            <FormKit type="text" name="placeName" label="Abfahrtort" />
            <FormKit type="text" name="arrivalAddress" label="Zielort" />
          </div>
          <div class="grow">
            <FormKit
              type="number"
              name="pricePerKilometer"
              label="Max. Kilometerpauschale"
            />
            <FormKit
              type="checkbox"
              label="Sonstiges"
              name="other"
              :options="{
                pets: 'Haustiere',
                smoker: 'Raucher Fahrzeug',
                coronaHygiene: 'Corona Hygiene Regeln',
              }"
            />
            <FormKit
              type="checkbox"
              label="Zahlungsmethoden"
              name="other"
              :options="{
                cash: 'Barzahlung',
                paypal: 'PayPal',
              }"
            />
          </div>
        </div>
      </FormKit>
    </div>
    <div>
      <RideListing v-for="ride in data.rides" :ride="ride" />
    </div>
  </main>
</template>