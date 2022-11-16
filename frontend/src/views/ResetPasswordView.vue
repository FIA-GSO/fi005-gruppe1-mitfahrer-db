<script lang="ts">
import { API } from '@/utils/utils';

// import TheWelcome from '../components/TheWelcome.vue'
export default {
  methods: {
    async submit(data: any) {
      try {
        const response = await API("reset-password", "POST", JSON.stringify(data))
        

        let errormsg: string = ''
        switch (response.status) {
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
          'reset-password-form',
          [errormsg]
        )

      } catch (error: any) {
        this.$formkit.setErrors(
          'reset-password-form',
          ['Entschuldigung, der Server konnte nicht erreicht werden. Bitte versuchen Sie es später erneut.']
        )
      }

    }
  }
}

</script>

<template>
  <div class="bg-white grow w-screen flex items-center justify-center">
    <div
      class="container bg-white xs:rounded-none sm:rounded sm:max-w-md xs:w-screen w-md center sm:border-2 sm:border-gray-400 p-8 flex flex-col align-center">
      <FormKit type="form" @submit="submit" id="register-form" class="flex flex-col"
        submit-label="Passwort zurücksetzen">
        <h1 class="font-sans dont-bold text-3xl text-center pb-8">
          Passwort zurücksetzen
        </h1>
        <p class="pb-8">Bitte geben Sie Ihre GSO-E-Mail-Adresse ein.
          <br><br>Anschließend wird eine E-Mail mit weiteren Anweisungen, um ein neues Passwort zu erstellen, gesendet.
        </p>
        <FormKit type="text" name="email" validation="required|email" label="GSO-E-Mail-Adresse"
          class="bg-gray-200 rounded h-16 px-8 mb-8 text-l outline-1 outline-gray-600"></FormKit>
      </FormKit>
    </div>
  </div>
</template>
