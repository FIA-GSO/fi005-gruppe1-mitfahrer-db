<script setup lang="ts">
import { useRouter } from "vue-router";

const router = useRouter();

async function submit(data: any) {
  try {
    const response = await fetch("http://127.0.0.1:5000/reset-password", {
      method: "POST",
      credentials: "include",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    }).then((r) => {
      if (!r.ok) {
        throw new Error("a");
      }
      return r.json();
    });

    const authToken = response.tempAuthToken;
    router.push({
      path: "/reset-password-confirm",
      query: {
        token: authToken,
      },
    });
  } catch (e) {
    console.error("Exception in reset password", e);
  }
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
        <p class="pb-8">
          Bitte geben Sie Ihre GSO-E-Mail-Adresse ein. <br /><br />Anschließend
          wird eine E-Mail mit weiteren Anweisungen, um ein neues Passwort zu
          erstellen, gesendet.
        </p>
        <FormKit
          type="text"
          name="email"
          validation="required|email"
          label="GSO-E-Mail-Adresse"
          class="bg-gray-200 rounded h-16 px-8 mb-8 text-l outline-1 outline-gray-600"
        ></FormKit>
      </FormKit>
    </div>
  </div>
</template>
