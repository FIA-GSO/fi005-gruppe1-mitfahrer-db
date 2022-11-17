import { ref } from 'vue'
import { defineStore } from 'pinia'
import {API, getErrorMessage } from '@/utils/utils';

export const useUserStore = defineStore('user', () => {
  const user = ref<any>(null);
  async function getUser() {
    try {
      const response = await API("user-info")
      user.value = (await response.json()).user;
    } catch (error: any) {
      console.log(error)
    }
  }

  async function login(email: string, password: string) {
    const response = await API("login", "POST", JSON.stringify({email, password}))
    user.value = (await response.json()).user;
  }

  async function logout() {
    await API("logout")
    user.value = null
  }

  const initialized = ref(false);

  const onInitialized = new Promise<void>(resolve => {
    getUser().then(() => {
      initialized.value = true
      resolve();
    });
  })

  return { initialized, user, login, logout, onInitialized }
})

