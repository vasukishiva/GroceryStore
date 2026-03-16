<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()

onMounted(async () => {
  await auth.logout()
  router.replace('/')
})
</script>

<template>
  <div class="text-center mt-5">
    <h5>Logging out...</h5>
  </div>
</template>
