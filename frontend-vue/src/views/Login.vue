<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-card">
        <div class="login-header">
          <h1><i class="fas fa-route"></i> TaskVoyage</h1>
          <p>任务管理新体验</p>
        </div>

        <div class="mode-switch">
          <button
            :class="['mode-btn', { active: !isRegister }]"
            @click="isRegister = false"
          >
            登录
          </button>
          <button
            :class="['mode-btn', { active: isRegister }]"
            @click="isRegister = true"
          >
            注册
          </button>
        </div>

        <form @submit.prevent="handleSubmit">
          <div class="form-group" v-if="isRegister">
            <label for="username">用户名</label>
            <input
              type="text"
              id="username"
              v-model="form.username"
              placeholder="请输入用户名"
              required
              :class="{ 'error': errors.username }"
            />
            <div class="error-message" v-if="errors.username">
              {{ errors.username }}
            </div>
          </div>

          <div class="form-group" v-if="isRegister">
            <label for="phone">手机号</label>
            <input
              type="tel"
              id="phone"
              v-model="form.phone"
              placeholder="请输入手机号"
              required
              :class="{ 'error': errors.phone }"
            />
            <div class="error-message" v-if="errors.phone">
              {{ errors.phone }}
            </div>
          </div>

          <div class="form-group" v-if="!isRegister">
            <label for="loginIdentifier">{{ identifierLabel }}</label>
            <input
              type="text"
              id="loginIdentifier"
              v-model="form.loginIdentifier"
              :placeholder="identifierPlaceholder"
              required
              :class="{ 'error': errors.loginIdentifier }"
              @input="handleIdentifierInput"
            />
            <div class="error-message" v-if="errors.loginIdentifier">
              {{ errors.loginIdentifier }}
            </div>
          </div>

          <div class="form-group">
            <label for="password">密码</label>
            <input
              type="password"
              id="password"
              v-model="form.password"
              placeholder="请输入密码"
              required
              :class="{ 'error': errors.password }"
            />
            <div class="error-message" v-if="errors.password">
              {{ errors.password }}
            </div>
          </div>

          <div class="form-group" v-if="isRegister">
            <label for="confirmPassword">确认密码</label>
            <input
              type="password"
              id="confirmPassword"
              v-model="form.confirmPassword"
              placeholder="请再次输入密码"
              required
              :class="{ 'error': errors.confirmPassword }"
            />
            <div class="error-message" v-if="errors.confirmPassword">
              {{ errors.confirmPassword }}
            </div>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn btn-primary" :disabled="loading">
              <i v-if="loading" class="fas fa-spinner fa-spin"></i>
              {{ isRegister ? '注册' : '登录' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <div class="toast" v-if="toast.show" :class="toast.type">
      <i
        :class="toast.type === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle'"
      ></i>
      {{ toast.message }}
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { login, register } from '../utils/auth'

const router = useRouter()
const isRegister = ref(false)
const loading = ref(false)

const form = reactive({
  username: '',
  phone: '',
  loginIdentifier: '',
  password: '',
  confirmPassword: ''
})

const errors = reactive({
  username: '',
  phone: '',
  loginIdentifier: '',
  password: '',
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

const identifierLabel = computed(() => {
  const identifier = form.loginIdentifier.trim()
  if (identifier && identifier.length === 11 && /^\d+$/.test(identifier)) {
    return '手机号'
  }
  return '用户名'
})

const identifierPlaceholder = computed(() => {
  const identifier = form.loginIdentifier.trim()
  if (identifier && identifier.length === 11 && /^\d+$/.test(identifier)) {
    return '请输入手机号'
  }
  return '请输入用户名'
})

const handleIdentifierInput = () => {
  errors.loginIdentifier = ''
}

const validatePhone = (phone) => {
  const phoneRegex = /^1[3-9]\d{9}$/
  return phoneRegex.test(phone)
}

const validatePassword = (password) => {
  const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,16}$/
  return passwordRegex.test(password)
}

const validateForm = () => {
  let valid = true
  
  errors.username = ''
  errors.phone = ''
  errors.loginIdentifier = ''
  errors.password = ''
  errors.confirmPassword = ''
  
  if (isRegister.value) {
    if (!form.username.trim()) {
      errors.username = '用户名不能为空'
      valid = false
    } else if (form.username.length < 2 || form.username.length > 50) {
      errors.username = '用户名长度需在2-50个字符之间'
      valid = false
    }
    
    if (!form.phone) {
      errors.phone = '手机号不能为空'
      valid = false
    } else if (!validatePhone(form.phone)) {
      errors.phone = '请输入有效的手机号'
      valid = false
    }
  } else {
    if (!form.loginIdentifier.trim()) {
      errors.loginIdentifier = '请输入用户名或手机号'
      valid = false
    } else {
      const identifier = form.loginIdentifier.trim()
      if (identifier.length === 11 && /^\d+$/.test(identifier)) {
        if (!validatePhone(identifier)) {
          errors.loginIdentifier = '请输入有效的手机号'
          valid = false
        }
      } else {
        if (identifier.length < 2 || identifier.length > 50) {
          errors.loginIdentifier = '用户名长度需在2-50个字符之间'
          valid = false
        }
      }
    }
  }
  
  if (!form.password) {
    errors.password = '密码不能为空'
    valid = false
  } else if (!validatePassword(form.password)) {
    errors.password = '密码需包含大小写字母和数字，8-16位'
    valid = false
  }
  
  if (isRegister.value && form.password !== form.confirmPassword) {
    errors.confirmPassword = '两次输入的密码不一致'
    valid = false
  }
  
  return valid
}

const handleSubmit = async () => {
  if (!validateForm()) return
  
  loading.value = true
  
  try {
    if (isRegister.value) {
      const response = await register(
        form.username,
        form.phone,
        form.password
      )
      
      if (response.message) {
        showToast('注册成功，请登录', 'success')
        isRegister.value = false
        form.phone = ''
        form.password = ''
        form.confirmPassword = ''
      } else {
        let errorMsg = '注册失败'
        if (response.username && response.username.length > 0 && response.username[0].includes('具有 username 的 用户 已存在')) {
          errorMsg = '用户名重复'
        } else if (response.phone && response.phone.length > 0 && response.phone[0].includes('具有 phone 的 用户 已存在')) {
          errorMsg = '手机号重复'
        } else if (Object.keys(response).length > 0) {
          errorMsg = Object.values(response).flat().join('；')
        }
        showToast(errorMsg, 'error')
      }
    } else {
      const success = await login(form.loginIdentifier, form.password)
      
      if (success) {
        showToast('登录成功', 'success')
        
        setTimeout(() => {
          router.push('/')
        }, 1000)
      } else {
        showToast('登录失败，请检查账号密码', 'error')
      }
    }
  } catch (error) {
    showToast(error.message || '网络错误，请重试', 'error')
  } finally {
    loading.value = false
  }
}
</script>