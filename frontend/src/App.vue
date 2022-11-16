<script setup lang="ts">
import { RouterView } from "vue-router";
import HeaderView from "./views/HeaderView.vue";
</script>

<template>
  <HeaderView></HeaderView>
  <RouterView class="grow flex flex-col" />
</template>

<style>
#app {
  @apply h-screen;
  @apply flex;
  @apply flex-col;
}
</style>
