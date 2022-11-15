<script setup lang="ts">
import { RouterView } from "vue-router";
import { useUserStore } from "@/stores/user";
const userStore = useUserStore();
</script>

<template>
  <div
    class="flex bg-gso-blue text-2xl md:text-3xl lg:text-4xl p-4 text-white text-center justify-center relative"
  >
    <div>Mitfahrer-Datenbank</div>
    <div
      v-if="userStore.user"
      class="absolute top-0 right-4 bottom-0 flex items-center"
    >
      {{ userStore.user.email }}
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
