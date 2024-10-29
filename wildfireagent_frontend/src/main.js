import './assets/tailwind.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App);
const gmaps_api_key = import.meta.env.VITE_APP_API_KEY
const ws_url = import.meta.env.VITE_APP_WS_URL
const api_url = import.meta.env.VITE_APP_API_URL

app.config.globalProperties.$gmaps_api_key = gmaps_api_key
app.config.globalProperties.$ws_url = ws_url
app.config.globalProperties.$api_url = api_url

app.use(router)

app.mount('#app')