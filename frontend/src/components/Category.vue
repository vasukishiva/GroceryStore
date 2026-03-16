<script setup>
    import { ref } from 'vue';
    import Products from './Products.vue';   
    import { useAuthStore } from '@/stores/auth';
    import { useRouter } from 'vue-router';

    const router = useRouter();

    const authStore = useAuthStore();
    const isAdmin = authStore.getUserRoles().includes('admin');
    const token = authStore.getAuthToken();

    const props = defineProps(['category']);

    //const emit = defineEmits(['select']);
    const deleteCategory = async (categoryId) => {
        if (!isAdmin) {
            alert('You do not have permission to delete this category.');
            return;
        }

        try {
            const response = await fetch(`http://localhost:5000/categories/${categoryId}`, {
                method: 'DELETE',
                headers: {

                    'Authentication-Token': token
                }
            });

            if (response.ok) {
                alert('Category deleted successfully.');
                router.go(0);
                // Optionally, emit an event to notify parent component to refresh the category list
            } else {
                const errorData = await response.json();
                alert(`Error deleting category: ${errorData.message}`);
            }
        } catch (error) {
            console.error('Error deleting category:', error);
            alert('An error occurred while deleting the category.');
        }
    };

</script>

<template>
    <div class="container-fluid">
    <div class="row align-items-center">
        
        <div class="col-9">
            <RouterLink :to="`/category/${props.category.id}`" class="text-decoration-none text-dark">  
                <h3>{{props.category.name}}</h3>
                <p>{{props.category.description}}</p>
                <img v-if="props.category.image_file" :src="`/static/images/categories/${props.category.image_file}`" alt="Category Image" width="100" height="100">
            </RouterLink>
        </div>
        <div class="col-3 d-flex gap-2 justify-content-end" v-if="isAdmin">
            <RouterLink :to="`/edit-category/${props.category.id}`" class="btn btn-sm"><img src="/src/assets/images/edit.png" alt="Edit" width="20" height="20"></RouterLink>
            <button class="btn btn-sm" @click="deleteCategory(props.category.id)"><img src="/src/assets/images/delete.png" alt="Delete" width="20" height="20"></button>
        </div>
        <!-- <div class="d-flex justify-content-center my-4" v-if="isAdmin">
              <RouterLink class="btn btn-success m-2" to="/products">Add Products</RouterLink>

        </div> -->
    </div>
    <!--Display products here-->
    <!-- <div class="row md-3">
        
        <table class="table">
            <thead>
                <tr>
                    <th scope="col">Product Name</th>
                    <th scope="col">Price</th>
                </tr>
            </thead>
            <tbody>
                <Products v-for="product in props.category.products" :key="product.name" :product="product" />
                    
                
            </tbody>  
        </table>  
    </div>  -->
    
  </div>
</template>