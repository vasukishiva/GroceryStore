<template>
    <div class="container mt-4">

        <h3>My Orders</h3>

        <div v-if="orders.length === 0">
            No orders yet.
        </div>
        <div v-for="order in orders" :key="order.order_id" class="card mt-3 p-3">

            <h5>Order #{{ order.order_id }}</h5>

            <p>
                Status:
                <span
                :class="order.status === 'PAID' ? 'text-success' : 'text-warning'"
                >
                {{ order.status }}
                </span>
            </p>

            <p>Total: ₹{{ order.total_amount }}</p>

            <ul>
                <li v-for="item in order.items" :key="item.product_id">
                {{ item.product_name }} × {{ item.quantity }} — ₹{{ item.total_price }}
                </li>
            </ul>

            <button
            v-if="order.status !== 'PAID'"
            class="btn btn-success mt-2"
            @click="pay(order.order_id)"
            >
            Pay Now
            </button>

        </div>



    </div>
</template>

<script setup>
    import { ref, onMounted, computed } from 'vue'
    import { useAuthStore } from '@/stores/auth'
    import { BASE_URL } from '@/config';
    import { useCartStore } from '@/stores/cart'

    const cartStore = useCartStore()

    const authStore = useAuthStore()

    const token = authStore.getAuthToken()


    const orders = ref([])
    async function fetchOrders(){
        const res = await fetch(`${BASE_URL}/orders`, {
        method: 'GET',
        headers: {
            'Authentication-Token': token
        }
        
        })
        orders.value = await res.json()
    }

    onMounted(async () => {
        await fetchOrders()
    })




    async function pay(orderId){

    await fetch(`${BASE_URL}/fake_payment`,{
    method:"POST",
    headers:{
    "Content-Type":"application/json",
    "Authentication-Token": token
    },
    body:JSON.stringify({
    order_id:orderId
    })
    })

    alert("Payment Successful")

    await fetchOrders()   // reload orders
    await cartStore.fetchCart()
    }



</script>
