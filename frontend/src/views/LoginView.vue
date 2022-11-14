<script lang="ts">
// import TheWelcome from '../components/TheWelcome.vue'

export default {
    methods: {
        login () {},
        forgotPassword() {}
    },
    data () {
        return {
            email: '',
            password: ''
        }
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
        <div class="flex flex-col align-centercontainer bg-white xs:rounded-none sm:rounded sm:max-w-md mx-auto xs:w-screen md:w-auto center sm:border sm:border-gray-400 p-8">
            <h1 class="font-sans dont-bold text-3xl text-center pb-16">Einloggen</h1>
            <FormKit type="form" @submit="login" label="Login" class="flex flex-col align-center">
                <FormKit v-model="email" type="text" validation="required|email" label="GSO-E-Mail-Adresse" class="bg-gray-200 rounded h-16 px-8 mb-8 text-l outline-1 outline-gray-600"></FormKit>
                <FormKit v-model="password" type="password" validation="required" label="Passwort" class="bg-gray-200 rounded h-16 px-8 mb-8 text-l outline-1 outline-gray-600"></FormKit>
            </FormKit>
            <a href="#" v-on:click="forgotPassword" class="text-black text-center underline outline-none hover:text-gray-600 focus:text-gray-500">Passwort vergessen?</a>

        </div>
      </div>
  </main>
</template>
