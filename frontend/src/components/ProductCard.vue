<script setup>


import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { defineProps } from 'vue'
import { useCartStore } from '@/stores/cart';
import { BASE_URL } from '@/config';



const router = useRouter();
const cartStore = useCartStore();
const authStore = useAuthStore();


const props = defineProps({
    product: { type: Object, required: true }
});

const isAdmin = authStore.getUserRoles().includes('admin');
const token = authStore.getAuthToken();





const deleteProduct = async (productId) => {
    if (!isAdmin) {
        alert('You do not have permission to delete this product.');
        return;
    }

    try {
        const response = await fetch(`${BASE_URL}/products/${productId}`, {
            method: 'DELETE',
            headers: {
                'Authentication-Token': token
            }
        });

        if (response.ok) {
            alert('Product deleted successfully.');
            router.go(0);
        } else {
            const errorData = await response.json();
            alert(`Error deleting product: ${errorData.message}`);
        }
    } catch (error) {
        console.error('Error deleting product:', error);
        alert('An error occurred while deleting the product.');
    }
};

const addToCart = async () => {
    if (!authStore.isAuthenticated) {
        alert('Please log in to add products to your cart.');
        router.push('/login');
        return;
    }

    try {
        const response = await fetch(`${BASE_URL}/user_cart`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': token
            },
            body: JSON.stringify({ product_id: props.product.id, quantity: 1 })
        });

        const data = await response.json();
        await cartStore.fetchCart();
        if (response.ok) {
            alert('Product added to cart successfully.');
        } else {
            const errorData = await response.json();
            alert(`Error adding product to cart: ${errorData.message}`);
        }
    } catch (error) {
        console.error('Error adding product to cart:', error);
        alert('An error occurred while adding the product to the cart.');
    }
};
</script>

<template>
    <div class="card h-100 shadow-sm">
        <!-- offer badge -->
        <span
            v-if="product.is_offer"
            class="badge bg-danger position-absolute top-0 start-0 m-2"
            style="font-size:14px"
        >
            {{ product.offer_percentage }}% OFF
        </span>

        <!-- <div v-if="product.is_offer" class="position-absolute top-0 start-0 bg-danger text-white p-2 rounded">
            Offer
        </div> -->
        <!-- Product Image -->
        <img
            v-if="product.image_file"
            :src="`${BASE_URL}/static/uploads/products/${product.image_file}`"
            class="card-img-top"
            alt="Product Image"
            
        />
        <div class="card-body d-flex flex-column">
            <!-- Product Name -->
            <h5 class="card-title">{{ product.name }}</h5>
            <!-- Product Description -->
            <p class="card-text flex-grow-1">{{ product.description }}</p>
            <!-- Product Price -->
            <h6 class="card-subtitle mb-2 text-muted">₹ {{ product.price }}</h6>
            <!-- Admin Actions -->
            <div class="mt-3" v-if="isAdmin">
                <RouterLink :to="`/products/${product.id}`" class="btn btn-sm btn-primary me-2">Edit</RouterLink>
                <button class="btn btn-sm btn-danger" @click="deleteProduct(product.id)">Delete</button>
            </div>
            <div class="mt-3" v-else>
                <button class="btn btn-sm btn-success" @click="addToCart">Add to Cart</button>
            </div>
        </div>
    </div>
    </template>
<style scoped>
.card:hover {
    transform: scale(1.02);
    transition: 0.2s ease;
}
.card-img-top {
    border-bottom: 1px solid #ddd;
    height: 140px;   /* reduce image size */
    object-fit: cover;
}
.card-body {
    display: flex;
    flex-direction: column;
    justify-content: space-between;

}
.btn {
    width: 100%;    
}   
.card {
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    height: 220px;   /* control total height */
    font-size: 14px;
}


</style>
    <!-- style="height: 200px; object-fit: cover;" -->