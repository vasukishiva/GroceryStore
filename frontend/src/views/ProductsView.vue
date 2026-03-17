<script setup>
    import ProductCard from '@/components/ProductCard.vue'
    
    import { ref, onMounted, computed, watch } from 'vue';
    import { useAuthStore } from '@/stores/auth'; 
    import { useRoute, useRouter } from 'vue-router';
    import { BASE_URL } from '@/config';
    
    const route = useRoute()
    const router = useRouter()
    const authStore = useAuthStore();
    const isAdmin = authStore.getUserRoles().includes('admin');
    const token = authStore.getAuthToken()

    const products = ref([])

    const isEdit = computed(() => !!route.params.id)

    const name = ref('')
    const description = ref('')
    const price = ref('')
    const stock = ref('')
    const image = ref(null)
    const categories = ref([])
    const category_id = ref('')

    const fetchCategories =  async () => {
        const res = await fetch(`${BASE_URL}/categories`)
        categories.value = await res.json()
    }

    const fetchProducts = async () => {
      const search = route.query.search || ''

      const res = await fetch(`${BASE_URL}/products?search=${search}`)
      products.value = await res.json()
    }

    // const fetchProducts = async () => {
    //     const res = await fetch('http://localhost:5000/products')
    //     products.value = await res.json()
    // }

    const loadProductForEdit = async (id) => {
      if(!id) return
      const res = await fetch(`${BASE_URL}/products/${id}`)
      const data = await res.json()
      name.value = data.name
      description.value = data.description
      price.value = data.price
      stock.value = data.stock
      image.value = data.image_file
      category_id.value = data.category_id
        
    }

    onMounted(async () =>{
        await fetchProducts()
        await fetchCategories()
        if (isEdit.value) {
          await loadProductForEdit(route.params.id)
        }
        //     const res = await fetch(`http://localhost:5000/products/${route.params.id}`)
        //     const data = await res.json()

        //     name.value = data.name
        //     description.value = data.description
        //     price.value = data.price
        //     stock.value = data.stock
        //     //image.value = data.image_file
            
        // }
    })

     const resetForm = () => {
        name.value = ''
        description.value =''
        price.value =''
        stock.value =''
        image.value = null
        category_id.value = ''
    }

      watch(() => route.params.id, async (newId) => {
          if (isEdit.value) {
            await loadProductForEdit(newId)
          } else {
            resetForm()
          }
        })

    const handleImageChange = (e) => {
        
        image.value = e.target.files[0]
    }

   

    async function submitProduct() {
        const formData = new FormData()
        formData.append('name', name.value)
        formData.append('description', description.value)
        formData.append('price', price.value)
        formData.append('stock', stock.value)
        
        formData.append('category_id', category_id.value) 


        if (image.value) {
            formData.append('image', image.value)
        }

        const url = isEdit.value ? `${BASE_URL}/products/${route.params.id}`: `${BASE_URL}/products`

        const method = isEdit.value ? 'PUT' : 'POST'

        const res = await fetch(url, {
            method,
            headers: {
                'Authentication-Token': token

            },
            body: formData
        })

        if (res.ok){
            alert(isEdit.value ? 'Product updated!' : 'Product added!')
            router.push('/products')
            await fetchProducts()
            resetForm()
        } else {
            alert('Failed to save product')
        }
    }

   
</script>
<template>
  <div class="container mt-4">

    <!-- ADMIN PRODUCT FORM -->
    <div v-if="isAdmin" class="card mb-4 p-4 shadow-sm">
      <h4>{{ isEdit ? 'Edit Product' : 'Add Product' }}</h4>

      <div class="mb-2">
        <input v-model="name" class="form-control" placeholder="Product Name" />
      </div>

      <div class="mb-2">
        <textarea v-model="description" class="form-control" placeholder="Description"></textarea>
      </div>

      <div class="mb-2">
        <input v-model="price" type="number" class="form-control" placeholder="Price" />
      </div>

      <div class="mb-2">
        <input v-model="stock" type="number" class="form-control" placeholder="Stock" />
      </div>
      <!--give dropdown for choosing category from the categories table-->

      <div class="mb-2">
        <select v-model="category_id" class="form-control">
          <option disabled value="">Select Category</option>
          <option v-for="category in categories" :key="category.id" :value="category.id">
            {{ category.name }}
          </option>
        </select>
      </div>

      

      

      <!-- <div class="mb-2">
        <input v-model="chooseCategory" type="number" class="form-control" placeholder="Category ID" />
      </div> -->

      <div class="mb-3">
        <input type="file" @change="handleImageChange" class="form-control" />
      </div>

      <button class="btn btn-primary" @click="submitProduct">
        {{ isEdit ? 'Update Product' : 'Add Product' }}
      </button>
    </div>

    <!-- PRODUCTS LIST -->
    <h3 class="mb-3">Products</h3>
    <div class="row row-cols-1 row-cols-md-3 g-4">
      <div class="col" v-for="product in products" :key="product.id">
        <ProductCard :product="product" />
      </div>
    </div>

  </div>
</template>


<!-- <template>
    <div>
        <h2 class="mb-4">Products</h2>
        <div class="row row-cols-1 row-cols-md-3 g-4">
            <div class="col" v-for="product in products">
                <ProductCard :product="product" />
            </div>
        </div>
    </div>
</template> -->
<style scoped>
</style>
