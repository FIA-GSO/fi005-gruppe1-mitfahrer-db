import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', () => {
  const user = ref<any>(null);
  async function getUser() {
    const response = await fetch("http://127.0.0.1:5000/user-info", {
      credentials: "include",
    }).then((r) => r.json());
    console.log(response);
    user.value = response.user;
  } 
  const initialized = ref(false);
  getUser().then(() => {
    initialized.value = true
  });
  return { initialized, user }
})

