import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
    },

    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue'),
    },

    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/logout',
      name: 'logout',
      component: () => import('../views/LogoutView.vue'),
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue'),
    },
    {
      path: '/add-category',
      name: 'add-category',
      component: () => import('../views/AddCategoryView.vue'),  
    },
    {
      path: '/edit-category/:id',
      name: 'edit-category',
      component: () => import('../views/EditCategoryView.vue'),  
    },
    {
      path: '/products',
      name: 'productsForm',
      component: () => import('../views/ProductsView.vue'),
    },
    {
      
      path: '/products/:id',
      name: 'productEdit',
      component: () => import('../views/ProductsView.vue'),
      props: true,
    },
    {
      path: '/manage-offers',
      name: 'manage-offers',
      component: () => import('../views/ManageOffersView.vue'),
    },
    {
      path: '/category/:id',
      name: 'CategoryProducts',
      component: () => import('../views/CategoryProducts.vue'),
    },
    {
      path: '/orders',
      name: 'orders',
      component: () => import('../views/OrdersView.vue'),

    },
    {
      path: '/offers/meta',
      name: 'offer-meta',
      component: () => import('../views/ManageOffersView.vue'),

    },
    
    {
      path: '/cart',
      name: 'cart',
      component: () => import('../views/CartView.vue'),
    }
    
    

    
  ],
})

export default router
