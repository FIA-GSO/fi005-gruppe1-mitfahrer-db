<script setup lang="ts">
import RideListing from "@/components/RideListing.vue";
import { API } from "@/utils/utils";
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
const router = useRouter();

const departureAddress = ref("");
const arrivalAddress = ref("");
const rideDirection = ref("to");

const data = reactive({
  rides: [],
});

async function submit(formData: any) {
  if (formData.direction === "from") {
    formData.address = formData.arrivalAddress;
  } else {
    formData.address = formData.departureAddress;
  }
  delete formData.departureAddress;
  delete formData.arrivalAddress;

  const response = await API(`rides/search?${new URLSearchParams(formData)}`);
  data.rides = (await response.json()).rides;
  console.log("search rides response", response);
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
    <div>
      <FormKit
        type="form"
        submit-label="Fahrt suchen"
        @submit="submit"
        validation-visibility="blur"
      >
        <div class="flex flex-col md:flex-row w-auto md:gap-8">
          <div class="grow">
            <FormKit
              type="date"
              name="date"
              label="Abfahrtsdatum"
              validation="required"
            />
            <div class="flex flex-row w-full gap-4 max-w-[25em]">
              <FormKit
                type="time"
                name="timeRangeStart"
                label="Von"
                outer-class="grow"
                validation="required"
              />
              <FormKit
                type="time"
                name="timeRangeEnd"
                label="Bis"
                outer-class="grow"
                validation="required"
              />
            </div>
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
          </div>
          <div class="grow">
            <FormKit
              type="number"
              name="pricePerKilometer"
              label="Max. Kilometerpauschale (€/km)"
              step="0.01"
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
              type="radio"
              label="Zahlungsmethoden"
              name="paymentMethod"
              validation="required"
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
      <RouterLink
        v-for="ride in data.rides"
        :to="{ name: 'rideDetails', params: { id: ride.id } }"
      >
        <RideListing :ride="ride" />
      </RouterLink>
    </div>
  </main>
</template>
