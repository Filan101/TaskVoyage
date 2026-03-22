<template>
  <div class="app-container">
    <header class="app-header">
      <div class="header-left">
        <h1><i class="fas fa-route"></i> TaskVoyage</h1>
      </div>
      <div class="header-right">
        <span class="user-info">{{ currentUser?.username }}</span>
        <button @click="goToHome" class="btn btn-secondary">
          <i class="fas fa-home"></i> 首页
        </button>
        <button @click="logout" class="btn btn-secondary">
          <i class="fas fa-sign-out-alt"></i> 退出
        </button>
      </div>
    </header>

    <main class="app-main profile-container">
      <div class="profile-header">
        <h2><i class="fas fa-user-circle"></i> 个人中心</h2>
      </div>

      <div class="profile-content">
        <!-- 修改密码模块 -->
        <div class="profile-section">
          <h3><i class="fas fa-lock"></i> 修改密码</h3>
          <form @submit.prevent="changePassword">
            <div class="form-group">
              <label for="currentPassword">当前密码</label>
              <input
                type="password"
                id="currentPassword"
                v-model="passwordForm.currentPassword"
                placeholder="请输入当前密码"
                required
              />
              <div class="error-message">{{ passwordErrors.currentPassword }}</div>
            </div>
            <div class="form-group">
              <label for="newPassword">新密码</label>
              <input
                type="password"
                id="newPassword"
                v-model="passwordForm.newPassword"
                placeholder="请输入新密码"
                required
                minlength="6"
              />
              <div class="error-message">{{ passwordErrors.newPassword }}</div>
            </div>
            <div class="form-group">
              <label for="confirmPassword">确认新密码</label>
              <input
                type="password"
                id="confirmPassword"
                v-model="passwordForm.confirmPassword"
                placeholder="请再次输入新密码"
                required
              />
              <div class="error-message">{{ passwordErrors.confirmPassword }}</div>
            </div>
            <div class="form-actions">
              <button
                type="submit"
                class="btn btn-primary"
                :disabled="changingPassword"
              >
                <i v-if="changingPassword" class="fas fa-spinner fa-spin"></i>
                修改密码
              </button>
            </div>
          </form>
        </div>

        <!-- 主题模式切换模块 -->
        <div class="profile-section">
          <h3><i class="fas fa-moon"></i> 主题设置</h3>
          <div class="theme-toggle">
            <span class="theme-label">白天模式</span>
            <label class="switch">
              <input
                type="checkbox"
                v-model="darkMode"
                @change="toggleTheme"
              />
              <span class="slider round"></span>
            </label>
            <span class="theme-label">黑夜模式</span>
          </div>
        </div>

        <!-- 任务统计模块 -->
        <div class="profile-section">
          <h3><i class="fas fa-chart-bar"></i> 任务统计</h3>
          <div class="task-stats">
            <div class="stat-card">
              <div class="stat-icon completed-icon">
                <i class="fas fa-check-circle"></i>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ completedTaskCount }}</div>
                <div class="stat-label">已完成任务</div>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-icon pending-icon">
                <i class="fas fa-clock"></i>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ pendingTaskCount }}</div>
                <div class="stat-label">待完成任务</div>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-icon total-icon">
                <i class="fas fa-list"></i>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ totalTaskCount }}</div>
                <div class="stat-label">总任务数</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <div class="toast" v-if="toast.show" :class="toast.type">
      <i
        :class="toast.type === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle'"
      ></i>
      {{ toast.message }}
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import dayjs from 'dayjs'
import api from '../utils/api'
import { getCurrentUser } from '../utils/auth'

const router = useRouter()
const currentUser = ref(null)
const tasks = ref([])
const changingPassword = ref(false)
const darkMode = ref(false)

const passwordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const passwordErrors = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const toast = reactive({
  show: false,
  message: '',
  type: 'success'
})

const showToast = (message, type = 'success') => {
  toast.message = message
  toast.type = type
  toast.show = true
  setTimeout(() => {
    toast.show = false
  }, 3000)
}

const loadTasks = async () => {
  try {
    const data = await api.tasks.getAll()
    tasks.value = Array.isArray(data) ? data : data.results || []
  } catch (error) {
    console.error('加载任务失败:', error)
  }
}

const completedTaskCount = computed(() => {
  return tasks.value.filter(t => t.status === 'completed').length
})

const pendingTaskCount = computed(() => {
  return tasks.value.filter(t => t.status !== 'completed').length
})

const totalTaskCount = computed(() => {
  return tasks.value.length
})

const formatRegisterTime = () => {
  if (!currentUser.value?.date_joined) return '未知'
  return dayjs(currentUser.value.date_joined).format('YYYY-MM-DD HH:mm:ss')
}

const changePassword = async () => {
  // 重置错误信息
  Object.keys(passwordErrors).forEach(key => {
    passwordErrors[key] = ''
  })

  // 验证表单
  if (!passwordForm.currentPassword) {
    passwordErrors.currentPassword = '当前密码不能为空'
    return
  }

  if (!passwordForm.newPassword) {
    passwordErrors.newPassword = '新密码不能为空'
    return
  }

  if (passwordForm.newPassword.length < 6) {
    passwordErrors.newPassword = '新密码长度至少为6位'
    return
  }

  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    passwordErrors.confirmPassword = '两次输入的密码不一致'
    return
  }

  changingPassword.value = true

  try {
    await api.auth.changePassword({
      old_password: passwordForm.currentPassword,
      new_password: passwordForm.newPassword
    })
    showToast('密码修改成功', 'success')
    
    // 清空表单
    Object.keys(passwordForm).forEach(key => {
      passwordForm[key] = ''
    })
  } catch (error) {
    // 显示后端返回的具体错误信息
    showToast(error.message || '密码修改失败', 'error')
  } finally {
    changingPassword.value = false
  }
}

const toggleTheme = () => {
  const html = document.documentElement
  if (darkMode.value) {
    html.classList.add('dark-mode')
    localStorage.setItem('theme', 'dark')
  } else {
    html.classList.remove('dark-mode')
    localStorage.setItem('theme', 'light')
  }
}

const goToHome = () => {
  router.push('/')
}

const logout = () => {
  api.auth.logout()
  router.push('/login')
}

onMounted(() => {
  currentUser.value = getCurrentUser()
  loadTasks()
  
  // 检查本地存储中的主题设置
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark') {
    darkMode.value = true
    document.documentElement.classList.add('dark-mode')
  }
})
</script>

<style scoped>
.profile-container {
  padding: 20px;
}

.profile-header {
  margin-bottom: 30px;
  padding-bottom: 15px;
  border-bottom: 2px solid #e0e0e0;
}

.profile-header h2 {
  font-size: 24px;
  color: #333;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 10px;
}

.profile-content {
  max-width: 800px;
  margin: 0 auto;
}

.profile-section {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.profile-section h3 {
  font-size: 18px;
  color: #333;
  margin: 0 0 20px 0;
  display: flex;
  align-items: center;
  gap: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e0e0e0;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #555;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.form-group input:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
}

.error-message {
  color: #f44336;
  font-size: 14px;
  margin-top: 5px;
}

.form-actions {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.theme-toggle {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 10px 0;
}

.theme-label {
  font-size: 16px;
  color: #555;
}

/* 开关样式 */
.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
  border-radius: 34px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #4CAF50;
}

input:focus + .slider {
  box-shadow: 0 0 1px #4CAF50;
}

input:checked + .slider:before {
  transform: translateX(26px);
}

/* 用户信息样式 */
.user-info-details {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
}

.info-label {
  font-weight: 500;
  color: #555;
}

.info-value {
  color: #333;
}

/* 任务统计样式 */
.task-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.stat-card {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  transition: transform 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
}

.completed-icon {
  background-color: #4CAF50;
}

.pending-icon {
  background-color: #ff9800;
}

.total-icon {
  background-color: #2196F3;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.stat-label {
  font-size: 14px;
  color: #666;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .profile-container {
    padding: 10px;
  }
  
  .profile-section {
    padding: 15px;
  }
  
  .task-stats {
    grid-template-columns: 1fr;
  }
}

/* 黑夜模式样式 */
.dark-mode .profile-section {
  background-color: #333;
  color: #f0f0f0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.dark-mode .profile-section h3 {
  color: #f0f0f0;
  border-bottom-color: #555;
}

.dark-mode .form-group label {
  color: #e0e0e0;
}

.dark-mode .form-group input {
  background-color: #444;
  border-color: #555;
  color: #f0f0f0;
}

.dark-mode .form-group input:focus {
  border-color: #4CAF50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.3);
}

.dark-mode .info-label {
  color: #e0e0e0;
}

.dark-mode .info-value {
  color: #f0f0f0;
}

.dark-mode .info-item {
  border-bottom-color: #555;
}

.dark-mode .stat-card {
  background-color: #444;
}

.dark-mode .stat-value {
  color: #f0f0f0;
}

.dark-mode .stat-label {
  color: #ccc;
}
</style>