<script setup lang="ts"></script>

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
        class="container p-12 bg-white xs:rounded-none sm:rounded sm:max-w-xl mx-auto xs:w-screen md:w-auto center sm:border-2 sm:border-gray-400"
      >
        <FormKit type="form" :actions="false">
          <div class="flex flex-col sm:flex-row justify-between">
            <div class="flex flex-col w-full sm:w-56">
              <FormKit type="text" label="Name" input-class="w-44 min-w-full" />
              <FormKit type="text" label="Vorname" />
              <FormKit type="password" label="Passwort" />
              <FormKit type="password" label="Passwort wiederholen" />
            </div>
            <div class="flex flex-col w-full sm:w-56">
              <FormKit type="date" label="Geburtsdatum" />
              <FormKit
                type="select"
                label="Geschlecht"
                :options="['männlich', 'weiblich', 'divers']"
              />
              <FormKit type="file" label="Profilbild" />
              <FormKit type="submit" input-class="!mt-6">Registrieren</FormKit>
            </div>
          </div>
        </FormKit>
      </div>
    </div>
  </main>
</template>
