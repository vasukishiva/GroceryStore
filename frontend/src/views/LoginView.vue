<template>
    <div class="container-fluid">
        <div class="row justify-content-center">
            <div class="col-6">
                <h1 class="text-center">Login</h1>
                <form @submit.prevent="login">
                        <div class="mb-3">
                            <label for="exampleInputEmail1" class="form-label">Email</label>
                            <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" v-model="email">
                            <div id="emailHelp" class="form-text">We'll never share your email with anyone else.</div>
                        </div>
                        <div class="mb-3">
                            <label for="exampleInputPassword1" class="form-label">Password</label>
                            <input type="password" class="form-control" id="exampleInputPassword1" v-model="password" @input="validatepassword">
                            <div id="passwordHelp" class="form-text">{{passwordError}}</div>

                        </div>
                        
                        <button type="submit" class="btn btn-primary">Submit</button>
                </form>
            </div>
        </div>
    </div>
</template>
<script setup>
import { ref } from 'vue';
import { useMessageStore } from '@/stores/errormessage';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';
import { BASE_URL } from '@/config';
const router = useRouter();

const messageStore = useMessageStore();
const authStore = useAuthStore();

const email = ref('');
const password = ref('');
const passwordError = ref('');

const validatepassword = () => {
    if(password.value.length < 6) {
        passwordError.value = "Password must be at least 6 characters long.";
        return false;
    } else {
        passwordError.value = "";
        return true;
        
    }
}
async function login() {
    if(!validatepassword()) {
        alert('Inavlid Password length')
        return
    }

    if(email.value ===''|| password.value ==='') {
        alert('Please fill all the fields');
        return;
    }

    const user ={
        
        email: email.value,
        password: password.value
    }

    const response = await fetch(`${BASE_URL}/api/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(user)
    });
    console.log(response);

    if(!response.ok) {
        const errorData = await response.json();
        console.error(errorData);
        alert('Login failed: ' + errorData.message);
        return;
    }
    else {
        const data = await response.json();
        console.log(data);
        const user = {
            id: data.user_details.id,
            email: data.user_details.email,
            roles: data.user_details.roles,
        };
        authStore.setUserCred(data.user_details.auth_token, user);
        
        //alert(data.message);
        messageStore.updateErrorMessages(data.message);
        router.push('/');
        

    }
        
}
</script>