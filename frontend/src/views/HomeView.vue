<script setup lang="ts">
// import TheWelcome from '../components/TheWelcome.vue'
</script>

<template>
  <main>
    <header>
      <div class="bg-gso-blue text-3xl md:text-4xl lg:text-5xl p-4 text-white text-center">Mitfahrer-Datenbank</div>
      <div class="flex flex-col md:flex-row md:items-center gap-4 md:gap-12">
        <img alt="Vue logo" class="logo h-20 max-w-max pl-4 md:pl-12" src="@/assets/cropped-LOGO-GSO_neu.png" />
        <div class="flex flex-row items-center gap-4 p-4 md:gap-12 md:h-24">
          <div><RouterLink to="/login">Einloggen</RouterLink></div>
          <div><RouterLink to="/login">Registrieren</RouterLink></div>
          <div><RouterLink to="/login">Benutzerhilfe</RouterLink></div>
        </div>
      </div>
      <div class="relative">
        <video id="wp-custom-header-video" autoplay loop playsinline class="w-100" src="@/assets/20201106_GSO-Loop_Herbst-Impressionen_1920x900.mp4"></video>
        <div class="absolute inset-0 flex items-center justify-center text-white text-center text-4xl md:text-5xl lg:text-6xl">Georg-Simon-Ohm-Berufskolleg</div>
      </div>
    </header>
    <img src="" />
  </main>
</template>
