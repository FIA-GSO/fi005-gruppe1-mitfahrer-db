import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { plugin, defaultConfig } from '@formkit/vue'
import { de } from "@formkit/i18n"
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import createAppRouter from './router'

import App from './App.vue'

import './assets/main.css'
import './main.css'
import '@formkit/themes/genesis'

const app = createApp(App)

app.use(plugin, defaultConfig({
  theme: 'genesis',
  locales: { de },
  locale: 'de'
}))
app.use(createPinia())
app.use(createAppRouter())

// Setup Font Awesome and add icons to the library
import { faCarSide, faCircleUser, faCircleQuestion, faSchool, faArrowRight, faDumpsterFire, faMars, faVenus, faGenderless } from '@fortawesome/free-solid-svg-icons'
library.add(faCarSide, faCircleUser, faCircleQuestion, faSchool, faArrowRight, faDumpsterFire, faMars, faVenus, faGenderless)
app.component('font-awesome-icon', FontAwesomeIcon)

app.mount('#app')
