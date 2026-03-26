<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { BASE_URL } from '@/config'
import ProductCard from '@/components/ProductCard.vue'

const authStore = useAuthStore()
const token = authStore.getAuthToken()
const email = authStore.getUserEmail()
const isAdmin = authStore.getUserRoles().includes('admin');

const recommendations = ref([])
const loading = ref(true)

async function fetchRecommendations() {
  try {
    const res = await fetch(`${BASE_URL}/recommendations`, {
      headers: {
        'Authentication-Token': token
      }
    })

    if (res.ok) {
      recommendations.value = await res.json()
    } else {
      console.error('Failed to fetch recommendations')
    }
  } catch (err) {
    console.error('Error:', err)
  } finally {
    loading.value = false
  }
}

onMounted(fetchRecommendations)
</script>

<template>
  <div class="container mt-5">

    <!-- Title -->
    <div class="d-flex justify-content-between align-items-center mb-3" v-if="!isAdmin">
      <h3>✨ Recommended for {{ email }}</h3>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center">
      Loading recommendations...
    </div>

    <!-- Empty -->
    <div v-else-if="recommendations.length === 0 && !isAdmin" class="alert alert-info">
      No recommendations available.
    </div>

    <!-- Products -->
    <div v-else class="row row-cols-1 row-cols-md-5 g-3">
      <div
        class="col"
        v-for="product in recommendations"
        :key="product.id"
      >
        <!--  Reuse of ProductCard -->
        <ProductCard :product="product" />
      </div>
    </div>

  </div>
</template>

<style scoped>
h4 {
  font-weight: bold;
}
</style>