import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { plugin, defaultConfig } from '@formkit/vue'

import App from './App.vue'
import router from './router'

import './assets/main.css'
import './main.css'
import '@formkit/themes/genesis'

const app = createApp(App)

app.use(plugin, defaultConfig({
  theme: 'genesis'
}))
app.use(createPinia())
app.use(router)


app.mount('#app')
