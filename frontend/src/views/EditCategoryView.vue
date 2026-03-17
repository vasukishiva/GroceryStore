<script setup>
import { useRoute } from 'vue-router';
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { BASE_URL } from '@/config';

const router = useRouter(); 

import { useAuthStore } from '@/stores/auth';
const route = useRoute();

const authStore = useAuthStore();
const categoryId = route.params.id;
const categoryMessage = ref('');
const category = ref(null);

onMounted(() => {
  // Fetch category details based on categoryId
  fetch(`${BASE_URL}/categories/${categoryId}`)
    .then(response => response.json())
    .then(data => {
      category.value = data;
    })
    .catch(error => {
      console.error('Error fetching category details:', error);
    });
});

if (!authStore.isAuthenticated || !authStore.getUserRoles().includes('admin')) {
    router.replace('/');
}


function validateCategory() {
    if(category.value.name.trim() === '') {
        categoryMessage.value = "Category name cannot be empty.";
        return false;
    } else {
        categoryMessage.value = "";
        return true;
        
    }
}

const editCategory = async (event) => {

  event.preventDefault();
    if(!validateCategory()) {
        alert('Invalid Category Name');
        return;
    }
  try {
    const response = await fetch(`${BASE_URL}/categories/${categoryId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': authStore.getAuthToken()
      },
      body: JSON.stringify({
        name: category.value.name,
        description: category.value.description,
      }),
    });

    if (response.ok) {
      alert('Category updated successfully.');
        router.push('/');
    } else {
      const errorData = await response.json();
      alert(`Error updating category: ${errorData.message}`);
    }
  } catch (error) {
    console.error('Error updating category:', error);
    alert('An error occurred while updating the category.');
  }
};
</script>
<template>
  <div v-if="category" class="container">
    <h2>Edit Category: {{ category.name }}</h2>
    <form>
      <div class="mb-3">
        <label for="categoryName" class="form-label">Category Name</label>
        <input type="text" class="form-control" id="categoryName" v-model="category.name">
      </div>
      <div class="mb-3">
        <label for="categoryDescription" class="form-label">Description</label>
        <textarea class="form-control" id="categoryDescription" v-model="category.description"></textarea>
      </div>
      <button type="submit" class="btn btn-primary" @click="editCategory">Save Changes</button>
    </form>
  </div>
  <div v-else class="container">
    <p>Loading category details...</p>
  </div>
</template>
<style scoped>
.container {
  max-width: 600px;
  margin-top: 20px;
}
.btn {
  margin-top: 10px;
}
</style>