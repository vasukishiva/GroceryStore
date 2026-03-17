<template>
    <div class="container-fluid">
        <div class="row justify-content-center">
            <div class="col-6 align-items-center">
                <h1 class="text-center">Register</h1>
                <form @submit.prevent="register">
                    <div class="mb-3">
                        <label for="exampleInputEmail1" class="form-label">Email</label>
                        <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" @blur="checkEmailAvailability" v-model="email">
                        <p class="form-text" v-if="checkEmailMessage">{{checkEmailMessage}} </p>
                        
                    </div>
                    <div class="mb-3">
                        <label for="exampleInputPassword1" class="form-label">Password</label>
                        <input type="password" class="form-control" id="exampleInputPassword1" v-model="password" @input="validatepassword">
                        <p class="form-text" v-if="passwordMessage">{{passwordMessage}}</p>
                    </div>
                    <button type="submit" class="btn btn-primary">Submit</button>
                </form>
            </div>
        </div>
    </div>
</template>
<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useMessageStore } from '@/stores/errormessage';
import { BASE_URL } from '@/config';

const messageStore = useMessageStore();

const router = useRouter();
const email = ref('');
const password = ref('');

const checkEmailMessage = ref('');
const passwordMessage = ref('');

function validatepassword() {
    if(password.value.length < 6) {
        passwordMessage.value = "Password must be at least 6 characters long.";
        return false;
    } else {
        passwordMessage.value = "";
        return true;
        
    }
}

function checkEmailAvailability() {

    if (email.value.includes('@')){
        fetch(`${BASE_URL}/api/check_email`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email: email.value })
        }).then(response => {
            if(response.ok) {
                return response.json();
            } else {
                console.error('Error checking email availability');
            }

        }).then(data => {
            if(data) {
                if(data.available) {
                    checkEmailMessage.value = 'Email is available';
                    
                } else {
                    checkEmailMessage.value = 'Email is already registered';
                }
            }
        });

    }
    else {
        checkEmailMessage.value = 'invalid email format';
    }

    // Here you can add logic to check if the email is already registered
    // For example, you can make an API call to your backend
    //console.log(`Checking availability for email: ${email.value}`);
}

async function register() {
    if(!validatepassword()) {
        alert('Invalid Password length')
        return
    }

    if(checkEmailMessage.value === 'Email is already registered') {
        alert('Email is already registered');
        return;
    }

    const user ={
        email: email.value,
        password: password.value
    }

    const response = await fetch(`${BASE_URL}/api/register`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(user)
    })
    if(!response.ok) {
        const errorData = await response.json();
        console.error(errorData);
        alert('Registration failed: ' + errorData.message);
        
    }
    else {
        const data = await response.json();
        console.log(data);
        //alert(data.message);
        messageStore.updateErrorMessages(data.message);
        router.push('/login');
    

    }
}
</script>