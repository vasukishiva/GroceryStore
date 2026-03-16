<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const token = authStore.getAuthToken()

const offerType = ref('product')
const selectedProduct = ref(null)
const selectedCategory = ref(null)
const offer_percentage = ref(10)
const offers = ref([])

const products = ref([])
const categories = ref([])

const fetchMeta = async () => {
  const res = await fetch('http://localhost:5000/offers/meta')
  const data = await res.json()
  console.log('meta data:', data)
  products.value = data.products
  categories.value = data.categories
}

const fetchOffers = async () => {
  const res = await fetch('http://localhost:5000/offers/list')
  offers.value = await res.json()
}
const deleteOffer = async (offer) => {

  if (offer.offer_type === 'product') {
    await fetch(`http://localhost:5000/offers/products/${offer.product_id}`, {
      method: 'DELETE',
      headers: {
        'Authentication-Token': token
      }
    })
  } else {
    await fetch(`http://localhost:5000/offers/categories/${offer.category_id}`, {
      method: 'DELETE',
      headers: {
        'Authentication-Token': token
      }
    })
  }

  fetchOffers()
}

// const deleteOffer = async (offerId) => {
//   if (offer.offer_type === 'product') {
//     await fetch(`http://localhost:5000/offers/products/${offerId}`, {
//       method: 'DELETE',
//       headers: {
//         'Authentication-Token': token
//       }
//     })
//   } else if (offer.offer_type === 'category') {
//     await fetch(`http://localhost:5000/offers/categories/${offerId}`, {
//       method: 'DELETE',
//       headers: {
//         'Authentication-Token': token
//       }
//     })
//   }
//   alert('Offer deleted successfully!')
//   fetchOffers()
// }
const submitOffer = async () => {
  const payload = {
    offer_type: offerType.value,
    offer_percentage: offer_percentage.value,
    product_id: offerType.value === 'product' ? selectedProduct.value : null,
    category_id: offerType.value === 'category' ? selectedCategory.value : null
  }

  await fetch('http://localhost:5000/offers', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authentication-Token': token
    },
    body: JSON.stringify(payload)
  })

  alert('Offer applied successfully!')
  fetchOffers()
}

onMounted(() => {
  fetchMeta()
  fetchOffers()
})
</script>

<template>
  <div class="container mt-4">
    <h2>Manage Offers</h2>

    <div class="mb-3">
      <label>Offer Type</label>
      <select v-model="offerType" class="form-select">
        <option value="product">Product</option>
        <option value="category">Category</option>
      </select>
    </div>

    <div class="mb-3" v-if="offerType === 'product'">
      <label>Select Product</label>
      <select v-model="selectedProduct" class="form-select">
        <option v-for="p in products" :key="p.id" :value="p.id">
          {{ p.name }}
        </option>
      </select>
    </div>

    <div class="mb-3" v-if="offerType === 'category'">
      <label>Select Category</label>
      <select v-model="selectedCategory" class="form-select">
        <option v-for="c in categories" :key="c.id" :value="c.id">
          {{ c.name }}
        </option>
      </select>
    </div>

    <div class="mb-3">
      <label>Offer Percentage (%)</label>
      <input type="number" v-model="offer_percentage" class="form-control" min="1" max="90" />
    </div>

    <button class="btn btn-success" @click="submitOffer">
      Apply Offer
    </button>
    <hr>

<h4>Active Offers</h4>

<table class="table table-bordered mt-3">

<thead>
<tr>
<th>Type</th>
<th>Name</th>
<th>Discount</th>
<th>Action</th>
</tr>
</thead>

<tbody>
<tr v-for="o in offers" :key="o.id">

<td>{{ o.offer_type }}</td>

<td>
{{ o.product_name || o.category_name }}
</td>

<td>{{ o.offer_percentage }}%</td>

<td>
<button class="btn btn-danger btn-sm" @click="deleteOffer(o)">
Remove
</button>
</td>

</tr>
</tbody>

</table>

  </div>
</template>






<!-- <script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import ProductCard from '@/components/ProductCard.vue';
const authStore = useAuthStore();
const isAdmin = authStore.getUserRoles().includes('admin');
const token = authStore.getAuthToken();
const offerProducts = ref([]);
//fetch offer products
const fetchOfferProducts = async () => {    
    try {
        const response = await fetch('http://localhost:5000/offers/products');
        if (!response.ok) {
        throw new Error('Failed to fetch offer products');
        }
        offerProducts.value = await response.json();
    } catch (error) {
        console.error('Error fetching offer products:', error);
    }
    };
onMounted(() => {
    fetchOfferProducts();
});


</script>
<template>
  <div>
    <!-- button to add offers to products -->
     <!-- button to add offers to category -->
     
  <!-- </div>
  <div>
    <h2 class="mb-4">Manage Offer Products</h2>
    <div v-if="offerProducts.length === 0">
      <p>No products are currently on offer.</p>
    </div>
    <div v-else class="row">
      <div v-for="product in offerProducts" :key="product.id" class="col-md-4 mb-4">
        <ProductCard :product="product" />
      </div>
    </div>
  </div>
</template> --> 
