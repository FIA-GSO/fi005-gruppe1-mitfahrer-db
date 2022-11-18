<script setup lang="ts">
import { API } from "@/utils/utils";
import { setErrors } from "@formkit/core";
import { useRouter } from "vue-router";

const router = useRouter();

async function submit(data: any) {
  try {
    const response = await API(
      "register",
      "POST",
      { email: data.email }
    );

    const authToken = await response.data.tempAuthToken;
    router.push({
      path: "/register-confirm",
      query: {
        token: authToken,
      },
    });
    console.log(response);
  } catch (e: any) {
    if (e.message === '409') {
      setErrors('register-form', ['Diese E-Mail-Adresse ist berets mit einem Konto verknüpft. Bitte logge dich stattdessen ein.'])
    }
  }
}
</script>

<template>
  <div class="bg-white grow w-screen flex items-center justify-center">
    <div
      class="container bg-white xs:rounded-none sm:rounded sm:max-w-md xs:w-screen w-md center sm:border-2 sm:border-gray-400 p-8 flex flex-col align-center overflow-y-auto"
    >
      <FormKit
        type="form"
        @submit="submit"
        id="register-form"
        class="flex flex-col"
        submit-label="Bestätigungslink senden"
      >
        <h1 class="font-sans dont-bold text-3xl text-center pb-8">
          Registrieren
        </h1>
        <p class="pb-8">
          Registrieren Sie sich bitte mit Ihrer GSO-E-Mail-Adresse. Sie bekommen
          anschließend eine Bestätigungs E-Mail. <br /><br />Nach erfolgreicher
          Bestätigung per E-Mail können Sie Ihre Personendaten vervollständigen.
        </p>
        <FormKit
          type="text"
          class="pb-8"
          name="email"
          validation="required|email|ends_with:@gso.schule.koeln"
          validation-visibility="blur"
          label="GSO-E-Mail-Adresse"
        ></FormKit>
      </FormKit>
      <span class="pb-4"
        >Haben Sie schon einen Account?
        <RouterLink
          to="/login"
          class="text-black text-center underline outline-none hover:text-gray-600 focus:text-gray-500"
          >Einloggen</RouterLink
        ></span
      >
      <FormKit
        type="button"
        label="Zurück"
        class="justify-self-end"
        @click="router.push({ path: '/' })"
      ></FormKit>
    </div>
  </div>
</template>
