<script setup lang="ts">
// import TheWelcome from '../components/TheWelcome.vue'
</script>

<template>
  <main>
    <header class="bg-white">
      <div class="flex flex-col md:flex-row md:items-center gap-4 md:gap-12">
        <img alt="Vue logo" class="logo h-20 max-w-max pl-4 md:pl-12" src="@/assets/cropped-LOGO-GSO_neu.png" />
      </div>
    </header>
    <div class="bg-white pt-8 h-full">
        <div class="container bg-white xs:rounded-none sm:rounded sm:max-w-md mx-auto xs:w-screen md:w-auto center sm:border-2 sm:border-gray-400">
            <form action="none" class="flex flex-col p-8">
                <h1 class="font-sans dont-bold text-3xl text-center pb-16">Einloggen</h1>
                <span class="pb-2">GSO-E-Mail-Adresse</span>
                <input type="text" class="bg-gray-200 rounded h-16 mb-8">
                <span class="pb-2">Passwort</span>
                <input type="text" class="bg-gray-200 rounded h-16 mb-8">
                <input type="submit" value="Login" class="bg-white rounded border-2 border-gray-400 h-16 text-xl">
            </form>
          
        </div>
      </div>
  </main>
</template>
