<script setup lang="ts">
import WelcomeView from "./WelcomeView.vue";
import HomeView from "./HomeView.vue";
import { useUserStore } from "@/stores/user";
const userStore = useUserStore();
</script>

<template>
  <WelcomeView v-if="!userStore.user" />
  <HomeView v-else />
</template>
