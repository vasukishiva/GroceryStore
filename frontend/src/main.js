//import './assets/main.css'

//create the app
import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)

// mount the app to the div with id 'app' in index.html
app.mount('#app')
