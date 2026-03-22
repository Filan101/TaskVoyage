import api from './api'

export const checkAuth = () => {
  const token = localStorage.getItem('access_token')
  const userStr = localStorage.getItem('user')
  
  if (!token || !userStr) {
    return false
  }
  
  try {
    const user = JSON.parse(userStr)
    return !!user && !!user.id
  } catch (e) {
    return false
  }
}

export const getCurrentUser = () => {
  const userStr = localStorage.getItem('user')
  if (userStr) {
    try {
      return JSON.parse(userStr)
    } catch (e) {
      return null
    }
  }
  return null
}

export const login = async (identifier, password) => {
  const response = await api.auth.login(identifier, password)
  
  if (response.access) {
    localStorage.setItem('access_token', response.access)
    localStorage.setItem('refresh_token', response.refresh)
    localStorage.setItem('user', JSON.stringify(response.user))
    return true
  }
  
  return false
}

export const register = async (username, phone, password) => {
  const response = await api.auth.register(username, phone, password)
  return response
}

export const logout = () => {
  api.auth.logout()
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user')
}