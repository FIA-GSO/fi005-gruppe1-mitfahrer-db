<script setup lang="ts">
import { API } from "@/utils/utils";
import { useRouter, useRoute } from "vue-router";

const router = useRouter();
const route = useRoute();

async function confirmResetRequest() {
  try {
    const response = API(`check-password-reset?token=${route.query.token}`);
    console.log(response);
    return response;
  } catch (e) {
    console.error(e);
  }
}
confirmResetRequest();

async function submit(formData: any) {
  formData.token = route.query.token;
  const response = await API("reset-password-confirm", "POST", formData);
  console.log(response);
  router.push({
    path: "/",
  });
}
</script>

<template>
  <div class="bg-white grow w-screen flex items-center justify-center">
    <div
      class="container bg-white xs:rounded-none sm:rounded sm:max-w-md xs:w-screen w-md center sm:border-2 sm:border-gray-400 p-8 flex flex-col align-center"
    >
      <FormKit
        type="form"
        @submit="submit"
        id="register-form"
        class="flex flex-col"
        submit-label="Passwort zurücksetzen"
      >
        <h1 class="font-sans dont-bold text-3xl text-center pb-8">
          Passwort zurücksetzen
        </h1>
        <FormKit
          type="text"
          name="newPassword"
          validation="required"
          label="Neues Passwort"
          class="bg-gray-200 rounded h-16 px-8 mb-8 text-l outline-1 outline-gray-600"
        ></FormKit>
        <FormKit
          type="text"
          validation="required|confirm:newPassword"
          validation-visibility="blur"
          label="Neues Passwort wiederholen"
          name="newPassword_confirm"
          class="bg-gray-200 rounded h-16 px-8 mb-8 text-l outline-1 outline-gray-600"
        ></FormKit>
      </FormKit>
    </div>
  </div>
</template>
