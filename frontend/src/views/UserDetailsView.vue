<script setup lang="ts">
import { useUserStore } from "@/stores/user";
import { API } from "@/utils/utils";
import { useRouter } from "vue-router";
const userStore = useUserStore();
const router = useRouter();

const toBase64 = (file: any) =>
  new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = (error) => reject(error);
  });

async function submit(formData: any) {
  console.log(formData);
  if (formData.image.length > 0) {
    let data = await toBase64(formData.image[0].file);
    formData.image = data.slice(data.indexOf("base64,") + 7);
  }

  const response = await API(
    "edit-user-details",
    "POST",
    formData
  );
  console.log("Edit response", response);
  userStore.user = response.data.user;
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
              label="Account-Typ"
              input-class="w-44 min-w-full"
              :value="userStore.user.type === 'student' ? 'Schüler' : 'Lehrer'"
              name="type"
              :disabled="true"
            />
            <FormKit
              type="text"
              label="Name"
              input-class="w-44 min-w-full"
              :value="userStore.user.lastName"
              name="lastName"
              validation="required"
            />
            <FormKit
              type="text"
              label="Vorname"
              :value="userStore.user.firstName"
              name="firstName"
              validation="required"
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
              validation="required"
            />
            <FormKit
              type="select"
              label="Geschlecht"
              :options="{'male': 'Männlich', 'female': 'Weiblich', 'other': 'Divers'}"
              :value="userStore.user.gender"
              name="gender"
            />
            <FormKit type="file" label="Profilbild" name="image" />
          </div>
        </div>
      </FormKit>
    </div>
  </div>
</template>
