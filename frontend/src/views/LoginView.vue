<script lang="ts">
// import TheWelcome from '../components/TheWelcome.vue'

export default {
    methods: {
        login () {},
        forgotPassword() {}
    }
}

</script>

<template>
  <main class="h-full">
    <header class="bg-white">
      <div class="flex flex-col md:flex-row md:items-center gap-4 md:gap-12">
        <RouterLink to="/" class="pl-4 md:pl-12 mx-auto lg:mx-0 p-2">
            <img alt="Vue logo" class="logo max-w-max h-20" src="@/assets/cropped-LOGO-GSO_neu.png" />
        </RouterLink>
        
      </div>
    </header>
    <div class="bg-white pt-8 h-full">
        <div class="container bg-white xs:rounded-none sm:rounded sm:max-w-md mx-auto xs:w-screen md:w-auto center sm:border-2 sm:border-gray-400">
            <form ref="form" v-on:submit.prevent="login" class="flex flex-col p-8">
                <h1 class="font-sans dont-bold text-3xl text-center pb-16">Einloggen</h1>
                <FormKit type="text" validation="required|email" label="GSO-E-Mail-Adresse" class="bg-gray-200 rounded h-16 px-8 mb-8 text-l outline-1 outline-gray-600"></FormKit>
                <FormKit type="password" validation="required" label="Passwort" class="bg-gray-200 rounded h-16 px-8 mb-8 text-l outline-1 outline-gray-600"></FormKit>
                <FormKit type="button" v-on:click="login" class="bg-white rounded border-2 border-gray-400 h-16 text-xl mb-8 hover:cursor-pointer hover:bg-gray-400 hover:text-white transition hover:ease-in-out active:bg-gray-600 outline-1 outline-gray-600">Login</FormKit>
                <a href="#" v-on:click="forgotPassword" class="text-black text-center underline outline-none	hover:text-gray-600 focus:text-gray-500">Passwort vergessen?</a>
            </form>
          
        </div>
      </div>
  </main>
</template>
