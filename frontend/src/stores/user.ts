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
  async function login(email: string, password: string) {
    const response = await fetch("http://127.0.0.1:5000/login", {
      method: "POST",
      credentials: "include",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email, password
      }),
    }).then(r => r.json());
    console.log(response);
    if (response.status === "success") {
      user.value = response.user;
    }
  }
  const initialized = ref(false);
  getUser().then(() => {
    initialized.value = true
  });
  return { initialized, user, login }
})

