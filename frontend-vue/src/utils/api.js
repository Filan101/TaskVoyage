const API_BASE_URL = '/api'

const api = {
  async request(endpoint, options = {}) {
    const token = localStorage.getItem('access_token')
    
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers
    }
    
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }
    
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers
    })
    
    if (response.status === 401) {
      const refreshToken = localStorage.getItem('refresh_token')
      if (refreshToken) {
        const refreshed = await this.refreshToken(refreshToken)
        if (refreshed) {
          return this.request(endpoint, options)
        }
      }
      this.logout()
      window.location.href = '/login'
      throw new Error('登录已过期')
    }
    
    if (!response.ok) {
      const error = await response.json().catch(() => ({}))
      throw new Error(error.error || error.detail || error.message || '请求失败')
    }
    
    const contentLength = response.headers.get('content-length')
    if (contentLength === '0' || !contentLength) {
      return {}
    }
    
    return response.json()
  },

  async refreshToken(refreshToken) {
    try {
      const response = await fetch(`${API_BASE_URL}/token/refresh/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ refresh: refreshToken })
      })
      
      if (response.ok) {
        const data = await response.json()
        localStorage.setItem('access_token', data.access)
        return true
      }
    } catch (e) {
      console.error('Token refresh failed:', e)
    }
    return false
  },

  auth: {
    async register(username, phone, password) {
      return fetch(`${API_BASE_URL}/auth/register/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, phone, password, password2: password })
      }).then(res => res.json())
    },

    async login(identifier, password) {
      const loginData = { password }
      if (/^\d{11}$/.test(identifier)) {
        loginData.phone = identifier
      } else {
        loginData.username = identifier
      }
      return fetch(`${API_BASE_URL}/token/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(loginData)
      }).then(res => res.json())
    },

    async getProfile() {
      return api.request('/auth/users/me/')
    },

    logout() {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
    },

    async changePassword(data) {
      return api.request('/auth/password/change/', {
        method: 'POST',
        body: JSON.stringify(data)
      })
    }
  },

  tasks: {
    async getAll(params = {}) {
      const queryString = new URLSearchParams(params).toString()
      return api.request(`/tasks/${queryString ? '?' + queryString : ''}`)
    },

    async getOne(id) {
      return api.request(`/tasks/${id}/`)
    },

    async create(data) {
      return api.request('/tasks/', {
        method: 'POST',
        body: JSON.stringify(data)
      })
    },

    async update(id, data) {
      return api.request(`/tasks/${id}/`, {
        method: 'PUT',
        body: JSON.stringify(data)
      })
    },

    async partialUpdate(id, data) {
      return api.request(`/tasks/${id}/`, {
        method: 'PATCH',
        body: JSON.stringify(data)
      })
    },

    async delete(id) {
      return api.request(`/tasks/${id}/`, {
        method: 'DELETE'
      })
    },

    async getStats() {
      return api.request('/tasks/stats/')
    }
  }
}

export default api