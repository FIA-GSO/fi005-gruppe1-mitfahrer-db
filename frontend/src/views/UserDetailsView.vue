<script setup lang="ts">
import { useRouter } from 'vue-router';

  const router = useRouter();
</script>

<template>
    <div class="bg-white w-screen flex items-center justify-center">
      <div
        class="container bg-white xs:rounded-none sm:rounded xs:w-screen sm:w-128 center sm:border-2 sm:border-gray-400 p-8 flex flex-col align-center"
      >
        <FormKit type="form" :actions="false">
          <h1 class="font-sans dont-bold text-3xl text-center pb-8">
            Personendaten bearbeiten
          </h1>
          <div class="flex flex-col sm:flex-row justify-between">
            <div class="flex flex-col w-full sm:w-56">
              <FormKit type="text" label="Name" input-class="w-44 min-w-full" />
              <FormKit type="text" label="Vorname" />
              <FormKit type="password" label="Neues Passwort" />
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
              
            </div>
            
          </div>
          <div class="flex justify-between">
              <FormKit type="button" input-class="!mt-6" @click="router.go(-1)">Abbrechen</FormKit>
              <FormKit type="submit" input-class="!mt-6">Änderungen speichern</FormKit>
              </div>
        </FormKit>
      </div>
    </div>
</template>
