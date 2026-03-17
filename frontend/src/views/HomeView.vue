<script setup>
import Category from '@/components/Category.vue';
import { useAuthStore } from '@/stores/auth';
import { onMounted, ref } from 'vue';
import ProductCard from '@/components/ProductCard.vue';
import { BASE_URL } from '@/config';

// import { useCartStore } from '@/stores/cart';

const auth = useAuthStore();
const isAdmin = auth.getUserRoles().includes('admin');
const categories = ref([]);
const latestProducts = ref([]);
const offerProducts = ref([]);
//const cartStore = useCartStore()

//fetch offer products
const fetchOfferProducts = async () => {
  try {
    const response = await fetch(`${BASE_URL}/offers/products`);
    if (!response.ok) {
      throw new Error('Failed to fetch offer products');
    }
    offerProducts.value = await response.json();
  } catch (error) {
    console.error('Error fetching offer products:', error);
  }
};
// Fetch categories from API 
fetch(`${BASE_URL}/categories`)
  .then(response => response.json())
  .then(data => {
    categories.value = data;
  })
  .catch(error => {
    console.error('Error fetching categories:', error);
  });

const fetchLatestProducts = async () => {
  try {
    const response = await fetch(`${BASE_URL}/products/latest`);
    if (!response.ok) {
      throw new Error('Failed to fetch latest products');
    }
    latestProducts.value = await response.json();
  } catch (error) {
    console.error('Error fetching latest products:', error);
  }
};

onMounted(() => {
  //cartStore.fetchCart()
  fetchLatestProducts();
  fetchOfferProducts();
});


</script>

<template>
  <div class="text-center mb-4">
    <h1 class="fw-bold">Welcome to the Grocery Store!</h1>
    <p class="text-muted">Find the best products at unbeatable prices.</p>
  </div>
  <div class="d-flex justify-content-between align-items-center mb-3">
  <h3 class="mb-0">Categories</h3>
  <div>
  <RouterLink class="btn btn-primary me-2" v-if="isAdmin" to="/add-category">Add Category</RouterLink>
  <RouterLink class="btn btn-secondary" v-if="isAdmin" to="/products">Add Products</RouterLink>
  </div>
</div>
  <!-- Horizontal scroll categories -->
<div class="category-scroll">
  <div
    class="category-item"
    v-for="category in categories"
    :key="category.id"
  >
    <Category :category="category" />
  </div>
</div>

<h3 class="mt-5 mb-3">Recently Added Products</h3>
<div class="row row-cols-1 row-cols-md-5 g-3">
  <div class="col" v-for="product in latestProducts" :key="product.id">
    <ProductCard :product="product" />
  </div>
</div>

<h3 class="mt-5 mb-3">Special Offers</h3>
<div v-if="isAdmin" class="d-flex justify-content-end mb-3 gap-2">
  <RouterLink class="btn btn-warning" to="/manage-offers">Manage Offers</RouterLink>
</div>

<div class="row row-cols-1 row-cols-md-5 g-3">
  <div class="col" v-for="product in offerProducts" :key="product.id">
    <ProductCard :product="product" />
  </div>
</div>



</template>
<style scoped>
.category-scroll {
  display: flex;
  gap: 1rem;
  overflow-x: auto;
  padding-bottom: 10px;
  scrollbar-width: none;
}

.category-scroll::-webkit-scrollbar {
  height: 6px;
  display: none;
}

.category-scroll::-webkit-scrollbar-thumb {
  background-color: #ccc;
  border-radius: 10px;
}

.category-item {
  min-width: 220px; /* controls card width */
  flex-shrink: 0;
  box-shadow: 10px 10px 20px rgba(0, 0, 0, 0.1);
  border-radius: 15px;
}
</style>
