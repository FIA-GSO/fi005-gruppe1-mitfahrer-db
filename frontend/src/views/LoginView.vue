<script setup lang="ts">
import { getNode, setErrors } from "@formkit/core";
import { useRouter, useRoute } from "vue-router";
import { useUserStore } from "@/stores/user";
const userStore = useUserStore();
const router = useRouter();

async function submit(data: any) {
  console.log("Submit", data);
  setErrors("login-form", [])
  try {
    await userStore.login(data.email, data.password)
    router.push({ path: "/" })
  } catch (error: any) {
    setErrors("login-form", [error.message])
  }
}
function forgotPassword(data: any) {
  console.log("forgotPassword", data)
}
</script>

<template>
    <div class="bg-white dark:text-white grow w-screen flex items-center justify-center">
      <div
        class="container xs:rounded-none sm:rounded sm:max-w-md xs:w-screen w-md center sm:border-2 sm:border-gray-400 p-8 flex flex-col align-center"
      >
        <FormKit
          type="form"
          @submit="submit"
          id="login-form"
          class="flex flex-col"
          submit-label="Login"
        >
          <h1 class="font-sans dont-bold text-3xl text-center pb-16">
            Einloggen
          </h1>
          <FormKit
            type="text"
            name="email"
            validation="required|email"
            label="GSO-E-Mail-Adresse"
            class="bg-gray-200 rounded h-16 px-8 mb-8 text-l outline-1 outline-gray-600"
          ></FormKit>
          <FormKit
            type="password"
            validation="required"
            name="password"
            label="Passwort"
            class="bg-gray-200 rounded h-16 px-8 mb-8 text-l outline-1 outline-gray-600"
          ></FormKit>
        </FormKit>
        <RouterLink
          to="/reset-password"
          v-on:click="forgotPassword"
          class="text-black text-center underline outline-none hover:text-gray-600 focus:text-gray-500 mb-8"
          >Passwort vergessen?
        </RouterLink>
        <FormKit label="Zurück zur Startseite" type="button" class="" @click="router.go(-1)"></FormKit>
      </div>
    </div>
</template>
