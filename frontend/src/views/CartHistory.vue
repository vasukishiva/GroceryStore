<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { BASE_URL } from '@/config'
import { useCartStore } from '@/stores/cart'

const cartStore = useCartStore()

const authStore = useAuthStore()
const token = authStore.getAuthToken()

const orders = ref([])

async function fetchOrders(){
  const res = await fetch(`${BASE_URL}/orders`, {
    headers: {
      'Authentication-Token': token
    }
  })
  orders.value = await res.json()
}

async function pay(orderId) {
  try {
    const res = await fetch(`${BASE_URL}/fake_payment`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authentication-Token": token
      },
      body: JSON.stringify({ order_id: orderId })
    })

    if (res.ok) {
      alert("Payment Successful ")
      await fetchOrders()
      await cartStore.fetchCart()   // update navbar count
    } else {
      alert("Payment failed ")
    }
  } catch (error) {
    console.error("Payment error:", error)
    alert("Something went wrong")
  }
}

async function deleteOrder(orderId) {
  const confirmDelete = confirm("Are you sure you want to delete this order?")

  if (!confirmDelete) return

  try {
    const res = await fetch(`${BASE_URL}/orders/${orderId}`, {
      method: "DELETE",
      headers: {
        "Authentication-Token": token
      }
    })

    if (res.ok) {
      alert("Order deleted successfully 🗑️")
      await fetchOrders()
      await cartStore.fetchCart()
    } else {
      alert("Failed to delete order")
    }
  } catch (error) {
    console.error("Delete error:", error)
    alert("Something went wrong")
  }
}

onMounted(fetchOrders)
</script>

<template>
  <div class="container mt-4">
    <h3> Cart History</h3>

    <div v-if="orders.length === 0" class="alert alert-info">
      No purchase history available.
    </div>

    <div 
      v-for="order in orders" 
      :key="order.order_id" 
      class="card mt-3 p-3 shadow-sm"
    >

      <div class="d-flex justify-content-between">
        <h5>Order #{{ order.order_id }}</h5>
        <small>{{ order.created_at }}</small>
      </div>

      <p>
        Status:
        <span 
          :class="order.status === 'PAID' ? 'text-success' : 'text-warning'"
        >
          {{ order.status }}
        </span>
      </p>

      <ul class="list-group">
        <li 
          v-for="item in order.items" 
          :key="item.product_id"
          class="list-group-item d-flex justify-content-between"
        >
          <span>{{ item.product_name }} × {{ item.quantity }}</span>
          <span>₹{{ item.total_price }}</span>
        </li>
      </ul>

      <div class="text-end mt-2 fw-bold">
        Total: ₹{{ order.total_amount }}
      </div>
      <div v-if="order.status !== 'PAID'" class="mt-3 d-flex gap-2">

        <!--  Pay -->
        <button
            class="btn btn-success btn-sm"
            @click="pay(order.order_id)"
        >
            Pay Now
        </button>

        <!--  Delete -->
        <button
            class="btn btn-danger btn-sm"
            @click="deleteOrder(order.order_id)"
        >
            Delete
        </button>

    </div>

    </div>
  </div>
</template>