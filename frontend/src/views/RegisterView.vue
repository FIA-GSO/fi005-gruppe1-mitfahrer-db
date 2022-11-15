<script lang="ts">
// import TheWelcome from '../components/TheWelcome.vue'
export default {
  methods: {
    async submit(data: any) {
      try {
        const res = await fetch("http://127.0.0.1:5000/register", {
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
          case 400:
            errormsg = "Entschuldigung, das hat nicht geklappt. Bitte geben Sie eine gültige GSO-E-Mail-Adresse ein."
            break
          case 409:
            errormsg = "Entschuldigung, die E-Mail-Addresse ist bereits mit einem Konto verknüpft. Bitte loggen Sie sich stattdessen ein."
            break
          case 500:
          case 502:
          case 404:
          case 403:
            errormsg = "Entschldigung, er Server kann die Anfrage im Moment nicht bearbeiten. Bitte versuchen Sie es später erneut."
            break
        }
        this.$formkit.setErrors(
          'register-form',
          [errormsg]
        )

      } catch (error: any) {
        this.$formkit.setErrors(
          'register-form',
          // fetch() wirft nur error bei Netzwerk-Problemen
          ['Entschuldigung, der Server konnte nicht erreicht werden. Bitte versuchen Sie es später erneut.']
        )
      }

    },
    login () {

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
    <div class="bg-white sm:pt-8 h-full">
      <div
        class="container bg-white xs:rounded-none sm:rounded sm:max-w-md mx-auto xs:w-screen md:w-auto center sm:border-2 sm:border-gray-400 p-8 flex flex-col align-center">
        <FormKit type="form" @submit="submit" id="register-form" class="flex flex-col" submit-label="Bestätigungslink senden">
          <h1 class="font-sans dont-bold text-3xl text-center pb-8">
            Registrieren
          </h1>
          <p class="pb-8">Registrieren Sie sich bitte mit Ihrer GSO-E-Mail-Adresse. Sie bekommen anschließend eine Bestätigungs E-Mail. 
            <br><br>Nach erfolgreicher Bestätigung per E-Mail können Sie Ihre Personendaten vervollständigen. 
            </p>
          <FormKit type="text" class="pb-8" name="email" validation="required|email" label="GSO-E-Mail-Adresse"></FormKit>
        </FormKit>
        <span class="pb-4">Haben Sie schon einen Account? <a href="#" v-on:click="login"
          class="text-black text-center underline outline-none hover:text-gray-600 focus:text-gray-500">Einloggen</a></span>
        <FormKit type="button" label="Zurück" class="justify-self-end"></FormKit>
      </div>
    </div>
  </main>
</template>
