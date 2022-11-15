<script lang="ts">
// import TheWelcome from '../components/TheWelcome.vue'
export default {
  methods: {
    async submit(data: any) {
      try {
        const res = await fetch("http://127.0.0.1:5000/login", {
          method: "POST",
          credentials: "include",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        });

        if (res.ok) {
          //TODO: Handle session store + redirect
          return
        }

        let errormsg: string = ''
        switch (res.status) {
          case 403:
            errormsg = "Entschuldigung, das hat nicht geklappt. Bitte prüfen Sie Ihre Anmeldedaten und versuchen Sie es erneut."
            break
          case 500:
          case 502:
          case 404:
            errormsg = "Entschldigung, er Server kann die Anfrage im Moment nicht bearbeiten. Bitte versuchen Sie es später erneut."
            break
        }
        this.$formkit.setErrors(
          'login-form',
          [errormsg]
        )

      } catch (error: any) {
        this.$formkit.setErrors(
          'login-form',
          // fetch() wirft nur error bei Netzwerk-Problemen
          ['Entschuldigung, der Server konnte nicht erreicht werden. Bitte versuchen Sie es später erneut.']
        )
      }

    },
    forgotPassword(data: any) {
      console.log("forgotPassword", data);
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
      <div
        class="container bg-white xs:rounded-none sm:rounded sm:max-w-md mx-auto xs:w-screen md:w-auto center sm:border-2 sm:border-gray-400 p-8 flex flex-col align-center">
        <FormKit type="form" @submit="submit" id="login-form" class="flex flex-col" submit-label="Login">
          <h1 class="font-sans dont-bold text-3xl text-center pb-16">
            Einloggen
          </h1>
          <FormKit type="text" name="email" validation="required|email" label="GSO-E-Mail-Adresse"
            class="bg-gray-200 rounded h-16 px-8 mb-8 text-l outline-1 outline-gray-600"></FormKit>
          <FormKit type="password" validation="required" name="password" label="Passwort"
            class="bg-gray-200 rounded h-16 px-8 mb-8 text-l outline-1 outline-gray-600"></FormKit>
        </FormKit>
        <a href="#" v-on:click="forgotPassword"
          class="text-black text-center underline outline-none hover:text-gray-600 focus:text-gray-500">Passwort
          vergessen?</a>
      </div>
    </div>
  </main>
</template>
