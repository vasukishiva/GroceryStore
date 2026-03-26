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
                <li v-if="authStore.isAuthenticated && authStore.getUserRoles().includes('user')">
                  <RouterLink to="/cart-history" class="dropdown-item">
                  Cart History
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
      <RouterLink to="/" class="text-white me-3">Home</RouterLink>
      <RouterLink to="/products" class="text-white me-3">Products</RouterLink>
      <RouterLink to="/contact" class="text-white">Contact</RouterLink>
      <RouterLink to="/about" class="text-white ms-3">About</RouterLink>
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
  /* background-image: url('@/assets/images/background.jpg'); */
  /* background-color: aquamarine;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;

}  */ 

/* background color */
body {
  background-color: #efeef5;
}
.custom-navbar {
  background: #72309e; /* dark blue */
  box-shadow: 0 4px 10px rgba(16, 15, 15, 0.1);
}

.navbar-brand {
  font-weight: bold;
  font-style: italic;
  font-size: 2.5rem;
  color: rgb(102, 42, 120) !important;
}

.nav-link {
  color: rgb(179, 125, 125) !important;
  font-size: 1.1rem;
}

.nav-link:hover {
  color: #ffd700 !important; /* gold hover */
}

.btn-outline-success {
  border-color: white;
  color: rgb(87, 33, 98);
}

.btn-outline-success:hover {
  background-color: white;
  color: #28a745;
}
.navbar {
  min-height: 60px;
  width: 118%;
  margin-left: -9%;
}



</style>
