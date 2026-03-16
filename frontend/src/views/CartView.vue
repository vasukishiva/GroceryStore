<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'
import { useRouter } from 'vue-router'

const router = useRouter()
const loading = ref(false)




const authStore = useAuthStore()
const token = authStore.getAuthToken()
const userId = authStore.getUserID()
const cartStore = useCartStore()

const cartItems = ref([])

async function checkout() {
  loading.value = true

  try {
    const res = await fetch(`http://localhost:5000/checkout`, {
      method: 'POST',
      headers: {
        'Authentication-Token': token
      }
    })

    if (res.ok) {
      alert('Checkout successful!')
      router.push('/orders')
    } else {
      alert('Checkout failed. Please try again.')
    }
  } catch (error) {
    console.error('Checkout error:', error)
    alert('An error occurred during checkout. Please try again.')
  } finally {
    loading.value = false
  }
}

const fetchCart = async () => {
  const res = await fetch(`http://localhost:5000/user_cart`, {
    method: 'GET',
    headers: {
      'Authentication-Token': token
    }
  })
//   cartItems.value = await res.json()
    const data = await res.json()
    console.log('CART DATA:', data)
    cartItems.value = data.items

}

onMounted(fetchCart)

// Increase / Decrease quantity
const updateQuantity = async (cartItemId, qty) => {
  if (qty < 1) return

  await fetch(`http://localhost:5000/user_cart/${cartItemId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authentication-Token': token
    },
    body: JSON.stringify({ quantity: qty })
  })

  fetchCart()
  await cartStore.fetchCart()
}

// Delete item
const deleteItem = async (cartItemId) => {
  await fetch(`http://localhost:5000/user_cart/${cartItemId}`, {
    method: 'DELETE',
    headers: {
      'Authentication-Token': token
    }
  })

  fetchCart()
  await cartStore.fetchCart()
}

const totalAmount = computed(() =>
  cartItems.value.reduce(
    (sum, item) => sum + item.total_price,
    0
  )
)
</script>
<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center">
    <h3 class="mb-0">Your Cart</h3>

    <button
      class="btn btn-success"
      @click="checkout"
    >
      Checkout
    </button>
  </div>


    <div v-if="cartItems.length === 0" class="alert alert-info">
      Your cart is empty
    </div>

    <table v-else class="table table-bordered align-middle">
      <thead>
        <tr>
          <th>Product</th>
          <th>Price</th>
          <th style="width:160px">Quantity</th>
          <th>Subtotal</th>
          <th>Action</th>
        </tr>
      </thead>

      <tbody>
            <tr v-for="item in cartItems" :key="item.id">
                <td>{{ item.product_name }}</td>

                <td>
                    <span class="fw-bold">₹ {{ item.final_price }}</span>
                    <div v-if="item.offer_percentage" class="small text-muted">
                        <del>₹ {{ item.base_price }}</del>
                        <span class="text-danger ms-1">
                            {{ item.offer_percentage }}% OFF
                        </span>
                    </div>
                </td>

                <td class="text-center">
                    <button
                        class="btn btn-sm btn-secondary me-1"
                        @click="updateQuantity(item.id, item.quantity - 1)"
                    >−</button>

                    {{ item.quantity }}

                    <button
                        class="btn btn-sm btn-secondary ms-1"
                        @click="updateQuantity(item.id, item.quantity + 1)"
                    >+</button>
                </td>

                <td>₹ {{ item.total_price }}</td>

                <td>
                    <button
                        class="btn btn-sm btn-danger"
                        @click="deleteItem(item.id)"
                >
                    Remove
                    </button>
                </td>
            </tr>

        <!-- <tr v-for="item in cartItems" :key="item.id">
          <td>{{ item.product_name }}</td>
          <td>₹ {{ item.price }}</td>

          <td class="text-center">
            <button
              class="btn btn-sm btn-secondary me-1"
              @click="updateQuantity(item.id, item.quantity - 1)"
            >−</button>

            {{ item.quantity }}

            <button
              class="btn btn-sm btn-secondary ms-1"
              @click="updateQuantity(item.id, item.quantity + 1)"
            >+</button>
          </td>

          <td>₹ {{ item.price * item.quantity }}</td>

          <td>
            <button
              class="btn btn-sm btn-danger"
              @click="deleteItem(item.id)"
            >
              Remove
            </button>
          </td>
        </tr> -->
      </tbody>
    </table>

    <div class="text-end fw-bold fs-5">
      Total: ₹ {{ totalAmount }}
    </div>
  </div>
</template>
