import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', () => {
  const isSignedIn = ref(false)
  function signIn() {
    isSignedIn.value = true;
  }
  return { isSignedIn, signIn }
})

