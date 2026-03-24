<script setup>
import { RouterLink, RouterView} from 'vue-router';
import { useMessageStore } from './stores/errormessage.js';
import { computed } from 'vue';
import { useAuthStore } from './stores/auth.js';
import { useCartStore } from './stores/cart.js';
import { onMounted, ref } from 'vue';
const messageStore = useMessageStore();
const authStore = useAuthStore();
const ErrorMessages = computed(() => messageStore.errorMessages);
const cartStore = useCartStore();

import { useRouter } from 'vue-router'

const router = useRouter()
const searchText = ref('')

const searchProduct = () => {
  router.push(`/products?search=${searchText.value}`)
}

onMounted(() => {
  cartStore.fetchCart()
})

const displayUserEmail = computed(() => {
  if (authStore.isAuthenticated) {
    return authStore.getUserEmail();
  }
  return '';
});
</script>

<template>
  <div class="container">
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <RouterLink class="navbar-brand" to="/"><img src="/src/assets/images/storelogo.png" alt="Grocery Store" width="30" height="30"/> Grocery Store</RouterLink>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <!--navbar content  -->
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            
            <!-- <li class="nav-item">
              <RouterLink class="nav-link" to="/about">About</RouterLink>
            </li> -->
            

            <li class="nav-item" v-if="authStore.isAuthenticated">
              <p class="nav-link">Hello, {{ displayUserEmail }}</p>
            </li>

            </ul>
           

          <!-- left links
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <RouterLink class="nav-link active" to="/login">Login</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link active" to="/register">Register</RouterLink>
            </li>
          </ul>-->

          <!-- search bar
            
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <RouterLink class="nav-link active" to="/login">Login</RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link active" to="/register">Register</RouterLink>
            </li>
            
          </ul>-->

          <form class="d-flex mx-auto" @submit.prevent="searchProduct">
            <input
              v-model="searchText"
              class="form-control me-2"
              type="search"
              placeholder="Type the product name"
            />

            <button class="btn btn-outline-success" type="submit">
              <img src="/src/assets/images/search.png" width="20" height="20"/>
            </button>
          </form>


          <!-- <form class="d-flex mx-auto" role="search">
            <input class="form-control me-2" type="search" placeholder="Type the product name" aria-label="Search"/>
            <button class="btn btn-outline-success" type="submit"><img src="/src/assets/images/search.png" alt="Search" width="20" height="20"/></button>
          </form> -->

          <!-- cart button-->
           <div v-if="!authStore.getUserRoles().includes('admin')">
           <RouterLink to="/cart" class="btn btn-outline-success"><img src="/src/assets/images/cart.png" alt="Cart" width="20" height="20"/> Cart ({{ cartStore.cartCount }})</RouterLink>
          </div>

           <!-- User Dropdown -->
          <ul class="navbar-nav">
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle p-0"
                 href="#"
                 role="button"
                 data-bs-toggle="dropdown"
                 aria-expanded="false">

                <img
                  src="/src/assets/images/user.png"
                  alt="User"
                  width="32"
                  height="32"
                  class="rounded-circle"
                />
              </a>

              <ul class="dropdown-menu dropdown-menu-end">
                <li v-if="!authStore.isAuthenticated">
                  <RouterLink class="dropdown-item" to="/login">
                    Login
                  </RouterLink>
                </li>
                <li v-if="!authStore.isAuthenticated">
                  <RouterLink class="dropdown-item" to="/register">
                    Register
                  </RouterLink>
                </li>
                <li v-if="authStore.isAuthenticated">
                  <RouterLink class="dropdown-item" to="/logout">
                    Logout
                  </RouterLink>
                </li>
                <li v-if="authStore.isAuthenticated">
                  <RouterLink class="dropdown-item" to="/profile">
                    Profile
                  </RouterLink>
                </li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div class="container-fluid">
      <p class="text-center mt-3" v-if="ErrorMessages">{{ ErrorMessages }}</p>
    </div>
    <RouterView/>
  </div>
  <footer class="bg-dark text-white py-4 mt-5">
  <div class="container text-center">
    
    <h5 class="mb-2">Grocery Store</h5>
    
    <p class="mb-2">
      Fresh groceries delivered to your doorstep 🛒
    </p>

    <div class="mb-2">
      <a href="/" class="text-white me-3">Home</a>
      <a href="/products" class="text-white me-3">Products</a>
      <a href="/contact" class="text-white">Contact</a>
      <a href="/about" class="text-white ms-3">About</a>
      
    </div>

    <p class="mb-0 small">
      © 2026 Grocery Store | Built with Vue & Flask
    </p>

  </div>
</footer>
   

</template>

<style>
/* background image */
/* .app-bg {
  min-height: 100vh;
  background-image: url('@/assets/images/background.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;

} */

</style>
