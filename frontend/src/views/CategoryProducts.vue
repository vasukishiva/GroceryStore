<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import ProductCard from '@/components/ProductCard.vue'
import { BASE_URL } from '@/config';

const route = useRoute()
const categoryId = route.params.id

const products = ref([])
const loading = ref(true)

const fetchProducts = async () => {
  try {
    const res = await fetch(
      `${BASE_URL}/categories/${categoryId}/products`
    )
    products.value = await res.json()
    console.log('Fetched products for category:', products.value)
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

onMounted(fetchProducts)
</script>

<template>
  <div class="container mt-4">
    <h3>Products</h3>

    <p v-if="loading">Loading...</p>

    <div class="row" v-else>
      <ProductCard
        v-for="product in products"
        :key="product.id"
        :product="product"
      />
    </div>
  </div>
</template>
<style scoped>
  /* product displayed medium size  grid way*/
  .row {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1rem;
  }
  
  
</style>