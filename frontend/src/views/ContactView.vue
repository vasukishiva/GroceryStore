<template>
  <div class="container mt-5">
    
    <h2 class="text-center mb-4">Contact Us</h2>

    <div class="row">
      
      <!-- Contact Form -->
      <div class="col-md-6">
        <form @submit.prevent="handleSubmit">
          
          <div class="mb-3">
            <label class="form-label">Name</label>
            <input type="text" v-model="form.name" class="form-control" required />
          </div>

          <div class="mb-3">
            <label class="form-label">Email</label>
            <input type="email" v-model="form.email" class="form-control" required />
          </div>

          <div class="mb-3">
            <label class="form-label">Message</label>
            <textarea v-model="form.message" class="form-control" rows="4" required></textarea>
          </div>

          <button class="btn btn-primary w-100">Send Message</button>

        </form>
      </div>

      <!-- Contact Info -->
      <div class="col-md-6">
        <h5>Our Details</h5>
        <p>📍 Chennai, India</p>
        <p>📞 +91 98765 43210</p>
        <p>📧 grocerystore@gmail.com</p>

        <hr />

        <p>
          We are here to help you with fresh groceries and fast delivery.
          Feel free to contact us anytime!
        </p>
      </div>

    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'

const form = reactive({
  name: '',
  email: '',
  message: ''
})

const handleSubmit = () => {
  alert("Message sent successfully! ")

  form.name = ''
  form.email = ''
  form.message = ''
}
</script>