<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useMessageStore } from '@/stores/errormessage';
import { useAuthStore } from '@/stores/auth';
import { BASE_URL } from '@/config';

const messageStore = useMessageStore();
const authStore = useAuthStore();
const router = useRouter();

// frontend role quard
if (!authStore.isAuthenticated || !authStore.getUserRoles().includes('admin')) {
    router.replace('/');
}

const categoryName = ref('');
const categoryDescription = ref('');
//const categoryImage = ref(null);
const categoryMessage = ref('');
function validateCategory() {
    if(categoryName.value.trim() === '') {
        categoryMessage.value = "Category name cannot be empty.";
        return false;
    } else {
        categoryMessage.value = "";
        return true;
        
    }
}
// function handleImageUpload(event) {
//     categoryImage.value = event.target.files[0];
// }

async function addCategory() {
    if(!validateCategory()) {
        alert('Invalid Category Name');
        return;
    }
    
    

    // const formData = new FormData();
    // formData.append('name', categoryName.value);
    // formData.append('description', categoryDescription.value);
    // if (categoryImage.value) {
    //     formData.append('image_file', categoryImage.value);
    // }

    const category = {
        name: categoryName.value,
        description: categoryDescription.value,
        //image: categoryImage.value

    };

    console.log('TOKEN:', authStore.getAuthToken())
    console.log('ROLES:', authStore.getUserRoles())


    const response = await fetch(`${BASE_URL}/categories`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': authStore.getAuthToken()
        },
        body: JSON.stringify(category)
    });
    if(!response.ok) {
        const errorData = await response.json();
        console.error(errorData);
        alert('Failed to add category: ' + errorData.message);
        return;
    } else {
        const data = await response.json();
        console.log(data);
        alert('Category added successfully!');
        router.push('/');
    }
}
</script>
<template>
  <div class="container mt-5">
    <h2>Add New Category</h2>
    <div class="mb-3">
      <label for="categoryName" class="form-label">Category Name</label>
      <input type="text" class="form-control" id="categoryName" v-model="categoryName" @input="validateCategory">
      <p class="form-text" v-if="categoryMessage">{{categoryMessage}}</p>   
    </div>
    <div class="mb-3">
      <label for="categoryDescription" class="form-label">Category Description</label>
      <textarea class="form-control" id="categoryDescription" v-model="categoryDescription"></textarea>
    </div>
    <!-- <div class="mb-3">
      <label class="form-label">Category Image</label>
      <input type="file" class="form-control" @change="handleImageUpload">
    </div> -->
    <button class="btn btn-primary" @click="addCategory">Add Category</button>
    </div>
</template>
<style scoped>
.form-text {
    color: red;
}

</style>