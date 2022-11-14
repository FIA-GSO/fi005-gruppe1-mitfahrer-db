<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
  <div class="flex-none bg-gso-blue text-3xl md:text-4xl lg:text-5xl p-4 text-white text-center">Mitfahrer-Datenbank</div>
  <RouterView class="grow flex flex-col"/>
</template>

<style>
  #app{
    @apply h-screen;
    @apply flex;
    @apply flex-col;
  }
</style>
