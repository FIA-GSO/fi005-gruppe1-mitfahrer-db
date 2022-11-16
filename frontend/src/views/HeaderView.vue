<script setup lang="ts">
import { useRouter } from "vue-router";
import { useUserStore } from "@/stores/user";
import Popup from "@/components/Popup.vue";
import { ref } from "vue";

const userPopup = ref(null)

const userStore = useUserStore();
const router = useRouter();

function logout() {
  userPopup.value.hidePopup()
  try {
    userStore.logout();
    router.push({ path: "/" });
  } catch (e) { }
}

function openUserHelp() {
  //TODO: Open user help
}

</script>

<template>
  <div class="flex bg-gso-blue dark:text-white text-2xl md:text-3xl lg:text-4xl p-4 md:p-3 text-white xxs:justify-center text-center relative h-16">
    <RouterLink to="/">Mitfahrer-Datenbank</RouterLink>
    <div class="absolute top-0 right-0 bottom-0 flex items-center justify-center">
      <a href="#" @click="openUserHelp" class="p-2 text-2xl hover:bg-white hover:text-gso-blue rounded-full w-12 h-12">
        <font-awesome-icon icon="fa-solid fa-circle-question" />
      </a>
      <a href="#" v-if="userStore.user" @click="$refs.userPopup.showPopup()" class="p-2 text-2xl hover:bg-white hover:text-gso-blue rounded-full w-12 h-12">
        <font-awesome-icon icon="fa-solid fa-circle-user" />
      </a>
      <Popup ref="userPopup">
        <div class="flex flex-col bg-white text-black items-end sm:items-center w-screen sm:w-64 sm:rounded-bl-lg">
          <div class="flex items-center w-full h-16 mb-4">
            <div class="grow text-right">
              <h1 class="text-lg">{{userStore.user.first_name}}</h1>
              <h1 class="text-xs">{{userStore.user.email}}</h1>
            </div>
            <a href="#" @click="$refs.userPopup.hidePopup()" class="p-2 text-2xl rounded-full w-12 h-12">
              <font-awesome-icon v-if="userStore.user" icon="fa-solid fa-circle-user" />
            </a>
          </div>
          <RouterLink to="/user-details" @click="$refs.userPopup.hidePopup()" class="text-sm mb-4 pr-4 sm:pr-0">Personendaten bearbeiten</RouterLink>
          <a href="#" @click="logout" class="text-sm mb-4 pr-4 sm:pr-0 text-red-500">Ausloggen</a>
        </div>

      </Popup>
    </div>

  </div>
</template>