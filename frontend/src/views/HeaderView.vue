<script setup lang="ts">
import { useRouter } from "vue-router";
import { useUserStore } from "@/stores/user";
import Popup from "@/components/Popup.vue";

const userStore = useUserStore();
const router = useRouter();

function logout() {
  console.log("Logout");
  try {
    userStore.logout();
    router.push({ path: "/" });
  } catch (e) { }
}
</script>

<template>
  <div class="flex bg-gso-blue text-2xl md:text-3xl lg:text-4xl p-4 text-white text-center justify-center relative h-16">
    <div>Mitfahrer-Datenbank</div>
    <div class="absolute top-0 right-0 bottom-0 flex items-center flex flex-col justify-center">
      <a href="#" @click="$refs.userPopup.showPopup()" class="p-2 text-2xl hover:bg-white hover:text-gso-blue rounded-full w-12 h-12">
        <font-awesome-icon v-if="userStore.user" icon="fa-solid fa-circle-user" />
      </a>
      <Popup ref="userPopup">
        <div class="flex flex-col bg-white text-black items-end sm:items-center w-screen sm:w-64 sm:rounded-bl-lg">
          <div class="flex items-center w-full h-16">
            <h1 class="grow text-lg text-right">Jakob</h1>
            <a href="#" @click="$refs.userPopup.hidePopup()" class="p-2 text-2xl rounded-full w-12 h-12">
              <font-awesome-icon v-if="userStore.user" icon="fa-solid fa-circle-user" />
            </a>
          </div>
          <a href="#" class="text-lg pb-4 pr-4 sm:pr-0">Kontodaten anzeigen</a>
          <a href="#" class="text-lg pb-2 pr-4 sm:pr-0 text-red-500">Ausloggen</a>
        </div>

      </Popup>
    </div>

  </div>
</template>