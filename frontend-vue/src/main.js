import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './styles/main.css'

// 检查本地存储中的主题设置
const savedTheme = localStorage.getItem('theme')
if (savedTheme === 'dark') {
  document.documentElement.classList.add('dark-mode')
}

createApp(App).use(router).mount('#app')