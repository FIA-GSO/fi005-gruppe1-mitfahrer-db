import { useUserStore } from '@/stores/user'
import LoginView from '@/views/LoginView.vue'
import { createRouter, createWebHistory } from 'vue-router'
import RootView from '../views/RootView.vue'
import RegisterDetailsView from '../views/RegisterDetailsView.vue'
import RegisterView from '@/views/RegisterView.vue'
import ResetPasswordView from '@/views/ResetPasswordView.vue'
import ResetPasswordConfirmView from '@/views/ResetPasswordConfirmView.vue'
import CreateRideView from '@/views/CreateRideView.vue'
import SearchRideView from '@/views/SearchRideView.vue'
import RideDetailView from '@/views/RideDetailView.vue'
import UserDetailsView from '@/views/UserDetailsView.vue'
import ErrorView from '@/views/ErrorView.vue'

const createAppRouter = () => {
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
        name: "register",
        component: RegisterView
      },
      {
        path: '/login',
        name: "login",
        component: LoginView
      },
      {
        path: '/reset-password',
        name: "resetPassword",
        component: ResetPasswordView
      },
      {
        path: '/reset-password-confirm',
        name: "resetPasswordConfirm",
        component: ResetPasswordConfirmView
      },
      {
        path: '/register-confirm',
        name: "registerConfirm",
        component: RegisterDetailsView
      },
      {
        path: '/rides/create',
        name: "createRide",
        component: CreateRideView
      },
      {
        path: '/rides/search',
        name: "searchRides",
        component: SearchRideView
      },
      {
        path: '/rides/detail/:id',
        name: "rideDetails",
        component: RideDetailView
      },
      {
        path: '/user-details',
        name: "userDetails",
        component: UserDetailsView
      },
      {
        path: '/error',
        name: "error",
        component: ErrorView
      }
    ]
  })

  router.beforeEach(async (to, from) => {
    const userStore = useUserStore()

    await userStore.onInitialized;

    if (!userStore.user && to.name !== "Login" && ["createRide", "searchRide", "rideDetails", "userDetails"].includes(to.name?.toString() || "")) {
      return {name: "login"}
    }
    return true
  })

  return router
}

export default createAppRouter
