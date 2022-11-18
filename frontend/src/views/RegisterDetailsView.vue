<script setup lang="ts">
import { useUserStore } from "@/stores/user";
import { API } from "@/utils/utils";
import { useRoute, useRouter } from "vue-router";
const route = useRoute();
const router = useRouter();
const userStore = useUserStore();

const toBase64 = (file: any) =>
  new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = (error) => reject(error);
  });

async function confirmRegistration() {
  const response = await API(`check-registration?token=${route.query.token}`);
  console.log(response);
  return response;
}
confirmRegistration();
async function submit(formData: any) {
  formData.token = route.query.token;
  if (formData.image.length > 0) {
    let data = await toBase64(formData.image[0].file);
    formData.image = data.slice(data.indexOf("base64,") + 7);
  }

  const response = await API("register-confirm", "POST", formData);
  console.log(response);
  userStore.user = response.data.user;
  router.push({
    path: "/",
  });
}
</script>

<template>
  <div class="bg-white grow w-screen flex items-center justify-center">
    <div
      class="container bg-white xs:rounded-none sm:rounded xs:w-screen sm:w-128 center sm:border-2 sm:border-gray-400 p-8 flex flex-col align-center"
    >
      <FormKit type="form" submit-label="Speichern" @submit="submit">
        <h1 class="font-sans dont-bold text-3xl text-center pb-8">
          Personendaten vervollständigen
        </h1>
        <div class="flex flex-col sm:flex-row justify-between">
          <div class="flex flex-col w-full sm:w-56">
            <FormKit
              type="text"
              label="Name"
              input-class="w-44 min-w-full"
              name="lastName"
              validation="required"
            />
            <FormKit
              type="text"
              label="Vorname"
              name="firstName"
              validation="required"
            />
            <FormKit
              type="password"
              label="Passwort"
              name="password"
              validation="required"
            />
            <FormKit
              type="password"
              name="password_confirm"
              label="Passwort wiederholen"
              validation="required|confirm:password"
              validation-visibility="blur"
            />
          </div>
          <div class="flex flex-col w-full sm:w-56">
            <FormKit
              type="date"
              label="Geburtsdatum"
              name="birthdate"
              validation="required"
            />
            <FormKit
              type="select"
              label="Geschlecht"
              :options="{
                male: 'Männlich',
                female: 'Weiblich',
                other: 'Divers',
              }"
              name="gender"
            />
            <FormKit type="file" label="Profilbild" name="image" />
            <FormKit
              type="checkbox"
              label="Datenschutzerklärung akzeptieren"
              validation="required"
            >
              <template #label="context">
                <label class="text-sm"
                  ><a class="underline text-sm" href="/Datenschutzerklärung.pdf"
                    >Datenschutzerklärung</a
                  >
                  akzeptiert</label
                >
              </template>
            </FormKit>
          </div>
        </div>
      </FormKit>
    </div>
  </div>
</template>
