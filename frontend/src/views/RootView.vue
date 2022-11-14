<script setup lang="ts">
import { ref } from 'vue'
import WelcomeView from './WelcomeView.vue';
import HomeView from './HomeView.vue';
import { useUserStore } from '@/stores/user'
const user = useUserStore();
</script>

<template>
  <WelcomeView v-if="!user.isSignedIn" />
  <HomeView v-else />
</template>
