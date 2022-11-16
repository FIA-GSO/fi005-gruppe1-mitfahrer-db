<script setup lang="ts">
import { API } from "@/utils/utils";
import { setErrors } from "@formkit/core";
import { ref } from "vue";
import { useRouter } from "vue-router";
const router = useRouter();

const departureAddress = ref("");
const arrivalAddress = ref("");
const rideDirection = ref("to");

async function submit(data: any) {
  if (data.direction === "from") {
    data.address = data.arrivalAddress;
  } else {
    data.address = data.departureAddress;
  }
  delete data.departureAddress;
  delete data.arrivalAddress;

  const response = await API("rides/create", "POST", JSON.stringify(data))
  if (response.ok) {
    router.push({
      path: "/",
    });
  }

}

function updateFromToFields() {
  if (rideDirection.value == "to") {
    departureAddress.value = arrivalAddress.value || "";
    arrivalAddress.value = "GSO";
  } else {
    arrivalAddress.value = departureAddress.value || "";
    departureAddress.value = "GSO";
  }
}
</script>

<template>
  <main class="bg-white p-8">
    <FormKit type="form" submit-label="Fahrt veröffentlichen" @submit="submit">
      <div class="flex flex-col md:flex-row w-auto md:gap-8">
        <div class="grow">
          <FormKit v-model="rideDirection" @input="updateFromToFields" type="radio" label="Fahrtrichtung"
            name="direction" :options="{ to: 'Hinfahrt', from: 'Rückfahrt' }" />
          <FormKit v-model="departureAddress" type="text" name="departureAddress" label="Abfahrtort"
            :disabled="rideDirection == 'from'" />
          <FormKit v-model="arrivalAddress" type="text" name="arrivalAddress" label="Zielort"
            :disabled="rideDirection == 'to'" />
          <FormKit type="number" name="pricePerKilometer" label="Kilometerpauschale" />
          <FormKit type="datetime-local" name="departureDateTime" label="Abfahrtszeitpunkt" />
        </div>
        <div class="grow">
          <FormKit type="text" name="carType" label="Autotyp" />
          <FormKit type="number" name="availableSeatCount" label="Freie Sitzplätze" />
          <FormKit type="checkbox" label="Sonstiges" name="other" :options="{
            pets: 'Haustiere',
            smoker: 'Raucher Fahrzeug',
            coronaHygiene: 'Corona Hygiene Regeln',
          }" />
        </div>
      </div>
    </FormKit>
  </main>
</template>
