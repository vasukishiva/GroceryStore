import { ref, computed } from 'vue'
import { defineStore } from 'pinia'


export const useAuthStore = defineStore('authStore', () => {
    const auth_token = ref(localStorage.getItem('token') || '')
    const user = ref(JSON.parse(localStorage.getItem('user')) || null)
    const isAuthenticated = computed(() => auth_token.value !== null && auth_token.value !== '')

    function setUserCred(token, userData) {
        localStorage.setItem('token', token)
        localStorage.setItem('user', JSON.stringify(userData))
        auth_token.value = token
        user.value = userData
    }

    function getUserID() {
        return user.value?.id || null
    }

    function clearAuthToken() {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        auth_token.value = null
        user.value = null
    }

    function getAuthToken() {
        return auth_token.value

    }

    function getUserEmail() {
        return user.value?.email || null
    }

    function getUserRoles() {
        return user.value?.roles || []
    }

    // logout function to clear token and user info

    async function logout() {
        try {
            await fetch('http://localhost:5000/api/logout', {
                method: 'POST',
                headers: {
                    
                    'Authentication-Token': auth_token.value
                }
            })
        } catch (error) {
            console.error('Logout failed:', error)
        }finally {
            clearAuthToken()
        }
    }

    return {isAuthenticated, setUserCred, clearAuthToken, getAuthToken, getUserEmail, getUserRoles, logout, getUserID}
})
