import LoginView from '@/views/LoginView.vue'
import { createRouter, createWebHistory } from 'vue-router'
import RootView from '../views/RootView.vue'
import RegisterDetailsView from '../views/RegisterDetailsView.vue'
import RegisterView from '@/views/RegisterView.vue'
import ResetPasswordView from '@/views/ResetPasswordView.vue'
import UserHelpView from '@/views/UserHelpView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: RootView
    },
    {
      path: '/register',
      component: RegisterView
    },
    {
      path: '/login',
      component: LoginView
    },
    {
      path: '/reset-password',
      component: ResetPasswordView
    },
    {
      path: '/help',
      component: UserHelpView
    },
    {
      path: '/register-confirm',
      component: RegisterDetailsView
    },
  ]
})

export default router
