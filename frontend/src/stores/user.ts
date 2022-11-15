import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

function getErrorMessage(status: Number) {
  switch (status) {
    case 403:
      return "Entschuldigung, das hat nicht geklappt. Bitte prüfen Sie Ihre Anmeldedaten und versuchen Sie es erneut.";
    case 500:
    case 502:
    case 404:
      return "Entschldigung, er Server kann die Anfrage im Moment nicht bearbeiten. Bitte versuchen Sie es später erneut.";
    default:
      return "Entschuldigung, der Server konnte nicht erreicht werden. Bitte versuchen Sie es später erneut.";
  }
}

export const useUserStore = defineStore('user', () => {
  const user = ref<any>(null);
  async function getUser() {
    const response = await fetch("http://127.0.0.1:5000/user-info", {
      credentials: "include",
    }).then(r => {
      if (!r.ok) {
        throw new Error(getErrorMessage(r.status));
      }
      return r.json();
    });
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
    }).then(r => {
      if (!r.ok) {
        throw new Error(getErrorMessage(r.status));
      }
      return r.json();
    });
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

