<script setup>
import Category from '@/components/Category.vue';
import { useAuthStore } from '@/stores/auth';
import { onMounted, ref } from 'vue';
import ProductCard from '@/components/ProductCard.vue';
import { BASE_URL } from '@/config';
import RecommendedProductView from '@/components/RecommendedProductView.vue';

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
  <br>
  <div class="text-center mb-4">
    <h1 class="fw-bold">Welcome to the Grocery Store!</h1>
    <p class="text-muted">Find the best products at unbeatable prices.</p>
  </div>
  <!-- adding images for slide show  -->
  <div id="carouselExampleIndicators" class="carousel slide mb-5" data-bs-ride="carousel">
    <div class="carousel-indicators">
      <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
      <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="1" aria-label="Slide 2"></button>
      <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="2" aria-label="Slide 3"></button>
    </div>
    <div class="carousel-inner">
      <div class="carousel-item">
        <img src="/src/assets/images/slides/slide1.avif" class="d-block w-100" alt="Fresh Produce">
        <div class="carousel-caption d-none d-md-block">
          <h5>Fresh Produce</h5>
          <p>Get the freshest fruits and vegetables delivered to your door.</p>
        </div>
      </div>
      <div class="carousel-item active">
        <img src="/src/assets/images/slides/slide2.jpg" class="d-block w-100" alt="Dairy Products">
        <div class="carousel-caption d-none d-md-block">
          <h5>Dairy Products</h5>
          <p>Discover our wide selection of milk, cheese, and yogurt.</p>
        </div>
      </div>
      <div class="carousel-item">
        <img src="/src/assets/images/slides/slide6.avif" class="d-block w-100" alt="Bakery Items">
        <div class="carousel-caption d-none d-md-block">
          <h5>Bakery Items</h5>
          <p>Indulge in our freshly baked bread, pastries, and cakes.</p>
        </div>
      </div>
    </div>
    <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="prev">
      <span class="carousel-control-prev-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Previous</span>
    </button>
    <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="next">
      <span class="carousel-control-next-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Next</span>
    </button>
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
<div class="d-flex justify-content-between align-items-center mb-3">
<h3 class="mt-5 mb-3">Recently Added Products</h3>
<div>
  
  <RouterLink class="btn btn-secondary" to="/products">View All Products</RouterLink>
  </div>
  </div>
<div class="row row-cols-1 row-cols-md-5 g-3">
  <div class="col" v-for="product in latestProducts" :key="product.id">
    <ProductCard :product="product" />
  </div>
</div>

<div v-if="!isAdmin">
    <!-- other sections -->
  
    <RecommendedProductView />
  

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
.carousel-inner img {
  height: 400px;
}

</style>
