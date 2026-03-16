import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useMessageStore = defineStore('messageStore', () => {
  const errorMessages = ref('')
  function updateErrorMessages(newMessage) {
    errorMessages.value = newMessage
    setTimeout(() => {
      errorMessages.value = ''
    }, 3000)
    
  }

  return { errorMessages, updateErrorMessages }
})
