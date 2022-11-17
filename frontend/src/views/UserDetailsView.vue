<script setup lang="ts">
import { useUserStore } from "@/stores/user";
import { useRouter } from "vue-router";
const userStore = useUserStore();
const router = useRouter();

async function submit(formData: any) {
  const response = await fetch("http://127.0.0.1:5000/edit-user-details", {
    method: "POST",
    credentials: "include",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  }).then((r) => {
    if (!r.ok) {
      throw new Error(`${r.status}`);
    }
    return r.json();
  });
  console.log("Edit response", response);
  userStore.user = response.user;
}
</script>

<template>
  <div class="bg-white w-screen flex items-center justify-center">
    <div
      class="container bg-white xs:rounded-none sm:rounded xs:w-screen sm:w-128 center sm:border-2 sm:border-gray-400 p-8 flex flex-col align-center"
    >
      <FormKit type="form" @submit="submit" submit-label="Änderungen speichern">
        <h1 class="font-sans dont-bold text-3xl text-center pb-8">
          Personendaten bearbeiten
        </h1>
        <div class="flex flex-col sm:flex-row justify-between">
          <div class="flex flex-col w-full sm:w-56">
            <FormKit
              type="text"
              label="Name"
              input-class="w-44 min-w-full"
              :value="userStore.user.lastName"
              name="lastName"
            />
            <FormKit
              type="text"
              label="Vorname"
              :value="userStore.user.firstName"
              name="firstName"
            />
            <FormKit
              type="password"
              label="Neues Passwort"
              name="newPassword"
            />
            <FormKit type="password" label="Passwort wiederholen" />
          </div>
          <div class="flex flex-col w-full sm:w-56">
            <FormKit
              type="date"
              label="Geburtsdatum"
              :value="userStore.user.birthdate"
              name="birthdate"
            />
            <FormKit
              type="select"
              label="Geschlecht"
              :options="['männlich', 'weiblich', 'divers']"
              :value="userStore.user.gender"
              name="gender"
            />
            <FormKit type="file" label="Profilbild" />
          </div>
        </div>
      </FormKit>
    </div>
  </div>
</template>
