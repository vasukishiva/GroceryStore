<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

const email = computed(() => auth.getUserEmail())
const roles = computed(() => auth.getUserRoles())

if (!auth.isAuthenticated) {
  router.replace('/login')
}
</script>

<template>
  <div class="container mt-5">
    <div class="card shadow-sm">
      <div class="card-body">
        <h4 class="card-title mb-3">My Profile</h4>

        <p>
          <strong>Email:</strong>
          <span>{{ email }}</span>
        </p>

        <p>
          <strong>Roles:</strong>
          <span v-if="roles.length">
            <span
              class="badge bg-success me-1"
              v-for="role in roles"
              :key="role"
            >
              {{ role }}
            </span>
          </span>
          <span v-else class="text-muted">No roles assigned</span>
        </p>

        <hr />

        <div class="d-flex gap-2">
          <RouterLink to="/" class="btn btn-outline-primary">
            Home
          </RouterLink>

          <RouterLink to="/logout" class="btn btn-outline-danger">
            Logout
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card {
  max-width: 500px;
  margin: auto;
}
</style>
