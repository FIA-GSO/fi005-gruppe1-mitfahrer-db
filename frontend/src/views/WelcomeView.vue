<script setup lang="ts">
import { useUserStore } from "@/stores/user";
const user = useUserStore();
</script>

<template>
  <main>
    <header class="bg-white">
      <div class="flex flex-col md:flex-row md:items-center gap-4 md:gap-12">
        <RouterLink :to="{name: 'home'}" class="pl-4 md:pl-12 mx-auto lg:mx-0 p-2 bm-2">
          <img
            alt="Vue logo"
            class="logo max-w-max h-20"
            src="@/assets/cropped-LOGO-GSO_neu.png"
          />
        </RouterLink>
        <div
          class="flex flex-row justify-center md:justify-start items-center gap-4 p-4 md:gap-12 md:h-24"
        >
          <div><RouterLink :to="{name: 'login'}">Einloggen</RouterLink></div>
          <div><RouterLink :to="{name: 'register'}">Registrieren</RouterLink></div>
        </div>
      </div>
      <div class="relative">
        <video
          id="wp-custom-header-video"
          autoplay
          loop
          muted
          playsinline
          class="w-100"
          src="@/assets/20201106_GSO-Loop_Herbst-Impressionen_1920x900.mp4"
        ></video>
        <div
          class="absolute inset-0 flex items-center justify-center text-white text-center text-4xl md:text-5xl lg:text-6xl"
        >
          Georg-Simon-Ohm-Berufskolleg
        </div>
      </div>
    </header>
  </main>
</template>
