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

  try {
    const response = await API("rides/create", "POST", data);
    if (response.ok) {
      router.push({
        path: "/",
      });
    }
  } catch (error: any) {}
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
          <FormKit
            v-model="rideDirection"
            @input="updateFromToFields"
            type="radio"
            label="Fahrtrichtung"
            name="direction"
            :options="{ to: 'Hinfahrt', from: 'Rückfahrt' }"
          />
          <FormKit
            v-model="departureAddress"
            type="text"
            name="departureAddress"
            label="Abfahrtort"
            :disabled="rideDirection == 'from'"
            validation="required"
          />
          <FormKit
            v-model="arrivalAddress"
            type="text"
            name="arrivalAddress"
            label="Zielort"
            :disabled="rideDirection == 'to'"
            validation="required"
          />
          <FormKit
            type="number"
            name="pricePerKilometer"
            label="Kilometerpauschale (€/km)"
            step="0.01"
            validation="required|between:0,0.3"
          />
          <FormKit
            type="datetime-local"
            name="departureDateTime"
            label="Abfahrtszeitpunkt"
            validation="required"
          />
        </div>
        <div class="grow">
          <FormKit type="text" name="carType" label="Autotyp" />
          <FormKit
            type="number"
            name="availableSeatCount"
            label="Freie Sitzplätze"
            validation="required"
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
            name="paymentMethods"
            :options="{
              cash: 'Barzahlung',
              paypal: 'PayPal',
            }"
            validation="required"
          />
        </div>
      </div>
    </FormKit>
  </main>
</template>
