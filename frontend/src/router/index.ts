import LoginView from '@/views/LoginView.vue'
import { createRouter, createWebHistory } from 'vue-router'
import RootView from '../views/RootView.vue'
import RegisterDetailsView from '../views/RegisterDetailsView.vue'
import RegisterView from '@/views/RegisterView.vue'
import ResetPasswordView from '@/views/ResetPasswordView.vue'
import CreateRideView from '@/views/CreateRideView.vue'
import SearchRideView from '@/views/SearchRideView.vue'
import RideDetailView from '@/views/RideDetailView.vue'
import UserDetailsView from '@/views/UserDetailsView.vue'

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
      path: '/register-confirm',
      component: RegisterDetailsView
    },
    {
      path: '/rides/create',
      component: CreateRideView
    },
    {
      path: '/rides/search',
      component: SearchRideView
    },
    {
      path: '/rides/detail/:id',
      component: RideDetailView
    },
    {
      path: '/user-details',
      component: UserDetailsView
    }
  ]
})

export default router
