import './assets/tailwind.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App);
const gmaps_api_key = import.meta.env.VITE_APP_API_KEY
app.config.globalProperties.$gmaps_api_key = gmaps_api_key

app.use(router)

app.mount('#app')