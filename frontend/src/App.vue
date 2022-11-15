<script setup lang="ts">
import { RouterView } from "vue-router";
import { useUserStore } from "@/stores/user";
import { useRouter } from "vue-router";

const router = useRouter();
const userStore = useUserStore();

function logout() {
  console.log("Logout");
  try {
    userStore.logout();
    router.push({ path: "/" });
  } catch (e) {}
}
</script>

<template>
  <div
    class="flex bg-gso-blue text-2xl md:text-3xl lg:text-4xl p-4 text-white text-center justify-center relative"
  >
    <div>Mitfahrer-Datenbank</div>
    <div
      v-if="userStore.user"
      class="absolute top-0 right-4 bottom-0 flex items-center text-lg flex flex-col justify-center"
    >
      {{ userStore.user.email }}
      <a href="#" class="underline" @click.prevent="logout">Abmelden</a>
    </div>
  </div>
  <RouterView class="grow flex flex-col" />
</template>

<style>
#app {
  @apply h-screen;
  @apply flex;
  @apply flex-col;
}
</style>
