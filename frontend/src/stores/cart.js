import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useAuthStore } from './auth'
import { BASE_URL } from '@/config';

export const useCartStore = defineStore('cart', () => {
  const cartItems = ref([])
  const authStore = useAuthStore()

  const cartCount = computed(() =>

    cartItems.value.reduce((sum, item) => sum + item.quantity, 0)
  )

  async function fetchCart() {
    if (!authStore.isAuthenticated) {
      cartItems.value = []
      return
    }


    const res = await fetch(`${BASE_URL}/user_cart`, {
      headers: {
        'Authentication-Token': authStore.getAuthToken()
      }
    })

    const data = await res.json()
    
    cartItems.value = data.items || []
  }

  return { cartItems, cartCount, fetchCart }
})














// import { ref, computed } from 'vue'
// import { defineStore } from 'pinia'
// import { useAuthStore } from './auth';



// export const useCartStore = defineStore('cart', {
//   state: () => ({
//     items: []
//   }),
//   getters: {
//     getCartItems: (state) => state.items,
//     getTotalPrice: (state) => {
//       return state.items.reduce((total, item) => total + (item.price * item.quantity), 0);
//     }
//   },
//   actions: {
//     addItem(item) {
//       const existingItem = this.items.find(i => i.id === item.id);
//       if (existingItem) {
//         existingItem.quantity += item.quantity;
//       } else {
//         this.items.push(item);
//       }
//     },
//     removeItem(itemId) {
//       this.items = this.items.filter(item => item.id !== itemId);
//     }
//   }
// });{ defineStore } 


