<template>
  <div class="app-container">
    <header class="app-header">
      <div class="header-left">
        <h1><i class="fas fa-route"></i> TaskVoyage</h1>
      </div>
      <div class="header-right">
        <router-link to="/profile" class="user-info">{{ currentUser?.username }}</router-link>
        <button @click="logout" class="btn btn-secondary">
          <i class="fas fa-sign-out-alt"></i> 退出
        </button>
      </div>
    </header>

    <nav class="app-nav">
      <button
        :class="['nav-btn', { active: currentView === 'next' }]"
        @click="currentView = 'next'"
      >
        <i class="fas fa-arrow-right"></i> 下一步
      </button>
      <button
        :class="['nav-btn', { active: currentView === 'honor' }]"
        @click="currentView = 'honor'"
      >
        <i class="fas fa-trophy"></i> 荣誉
      </button>
      <button
        :class="['nav-btn', { active: currentView === 'all' }]"
        @click="currentView = 'all'"
      >
        <i class="fas fa-list"></i> All
      </button>
    </nav>

    <main class="app-main">
      <div :class="['view', { active: currentView === 'next' }]">
        <div class="view-header">
          <h2><i class="fas fa-arrow-right"></i> 下一步</h2>
          <button @click="openTaskModal" class="btn btn-primary">
            <i class="fas fa-plus"></i> 新建任务
          </button>
        </div>
        <div class="task-grid" ref="taskGrid">
          <template v-if="nextTasks.length > 0">
            <div
              v-for="task in nextTasks"
              :key="task.id"
              :data-task-id="task.id"
              :class="['task-card', { completed: task.status === 'completed' }]"
              @click="expandTask(task)"
            >
              <img
                :src="getLazyImageSrc(task)"
                :alt="task.title"
                class="task-image"
                loading="lazy"
                @load="onImageLoad"
                @error="(event) => onImageError(event, task)"
              />
              <div class="task-content">
                <h3 class="task-title">{{ task.title }}</h3>
                <p class="task-desc">
                  {{ task.description || '暂无描述' }}
                </p>
                <div class="task-meta">
                  <div class="task-time">
                    <i class="fas fa-clock"></i>
                    <span :class="getTimeClass(task)">
                      {{ formatTime(task) }}
                    </span>
                  </div>
                  <div class="task-actions">
                    <button
                      v-if="task.status !== 'completed'"
                      @click.stop="completeTask(task)"
                      class="btn btn-small btn-primary"
                    >
                      完成
                    </button>
                    <button
                      @click.stop="editTask(task)"
                      class="btn btn-small btn-warning"
                    >
                      编辑
                    </button>
                    <button
                      @click.stop="confirmDeleteTask(task)"
                      class="btn btn-small btn-danger"
                    >
                      删除
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </template>
          <div v-else class="empty-state">
            <i class="fas fa-tasks"></i>
            <h3>暂无待完成任务</h3>
            <p>点击上方按钮创建新任务</p>
          </div>
        </div>
      </div>

      <div :class="['view', { active: currentView === 'honor' }]">
        <div class="view-header">
          <h2><i class="fas fa-trophy"></i> 荣誉</h2>
        </div>
        <div class="task-grid" ref="taskGrid">
          <template v-if="completedTasks.length > 0">
            <div
              v-for="task in completedTasks"
              :key="task.id"
              :data-task-id="task.id"
              class="task-card completed"
              @click="expandTask(task)"
            >
              <img
                :src="getLazyImageSrc(task)"
                :alt="task.title"
                class="task-image"
                loading="lazy"
                @load="onImageLoad"
                @error="(event) => onImageError(event, task)"
              />
              <div class="task-content">
                <h3 class="task-title">{{ task.title }}</h3>
                <p class="task-desc">
                  {{ task.description || '暂无描述' }}
                </p>
                <div class="task-meta">
                  <div class="task-time">
                    <i class="fas fa-check-circle"></i>
                    <span class="time-completed">已完成</span>
                  </div>
                  <div class="task-actions">
                    <button
                      @click.stop="uncompleteTask(task)"
                      class="btn btn-small btn-secondary"
                    >
                      恢复
                    </button>
                    <button
                      @click.stop="confirmDeleteTask(task)"
                      class="btn btn-small btn-danger"
                    >
                      删除
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </template>
          <div v-else class="empty-state">
            <i class="fas fa-trophy"></i>
            <h3>暂无已完成任务</h3>
            <p>完成一些任务来获得荣誉吧</p>
          </div>
        </div>
      </div>

      <div :class="['view', { active: currentView === 'all' }]">
        <div class="view-header">
          <h2><i class="fas fa-list"></i> All</h2>
          <div class="filter-controls">
            <select v-model="sortBy" class="select-control">
              <option value="name">名称排序</option>
              <option value="createdAt">创建时间</option>
              <option value="status">任务状态</option>
            </select>
            <select v-model="filterBy" class="select-control">
              <option value="all">全部</option>
              <option value="completed">已完成</option>
              <option value="pending">未完成</option>
            </select>
          </div>
        </div>
        <div class="task-grid" ref="taskGrid">
          <template v-if="filteredAllTasks.length > 0">
            <div
              v-for="task in filteredAllTasks"
              :key="task.id"
              :data-task-id="task.id"
              :class="['task-card', { completed: task.status === 'completed' }]"
              @click="expandTask(task)"
            >
              <img
                :src="getLazyImageSrc(task)"
                :alt="task.title"
                class="task-image"
                loading="lazy"
                @load="onImageLoad"
                @error="(event) => onImageError(event, task)"
              />
              <div class="task-content">
                <h3 class="task-title">{{ task.title }}</h3>
                <p class="task-desc">
                  {{ task.description || '暂无描述' }}
                </p>
                <div class="task-meta">
                  <div class="task-time">
                    <i class="fas fa-clock"></i>
                    <span :class="getTimeClass(task)">
                      {{ formatTime(task) }}
                    </span>
                  </div>
                  <div class="task-actions">
                    <button
                      v-if="task.status !== 'completed'"
                      @click.stop="completeTask(task)"
                      class="btn btn-small btn-primary"
                    >
                      完成
                    </button>
                    <button
                      v-else
                      @click.stop="uncompleteTask(task)"
                      class="btn btn-small btn-secondary"
                    >
                      恢复
                    </button>
                    <button
                      @click.stop="editTask(task)"
                      class="btn btn-small btn-warning"
                    >
                      编辑
                    </button>
                    <button
                      @click.stop="confirmDeleteTask(task)"
                      class="btn btn-small btn-danger"
                    >
                      删除
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </template>
          <div v-else class="empty-state">
            <i class="fas fa-clipboard-list"></i>
            <h3>暂无任务</h3>
            <p>点击上方按钮创建新任务</p>
          </div>
        </div>
      </div>
    </main>

    <div :class="['modal', { active: showTaskModal }]">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ editingTask ? '编辑任务' : '新建任务' }}</h3>
          <button class="close-btn" @click="closeTaskModal">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <form @submit.prevent="submitTask">
          <div class="form-group">
            <label for="taskTitle">任务名称</label>
            <input
              type="text"
              id="taskTitle"
              v-model="taskForm.title"
              placeholder="请输入任务名称"
              required
              ref="taskTitleInput"
            />
            <div class="error-message">{{ taskFormErrors.title }}</div>
          </div>
          <div class="form-group">
            <label for="taskDesc">任务描述</label>
            <textarea
              id="taskDesc"
              v-model="taskForm.description"
              rows="4"
              placeholder="请输入任务描述"
            ></textarea>
          </div>
          <div class="form-group">
            <label for="taskDeadline">期限（小时）</label>
            <input
              type="number"
              id="taskDeadline"
              v-model.number="taskForm.deadlineHours"
              min="1"
              max="8760"
            />
          </div>

          <div class="form-actions">
            <button
              type="button"
              @click="closeTaskModal"
              class="btn btn-secondary"
            >
              取消
            </button>
            <button
              type="submit"
              class="btn btn-primary"
              :disabled="submitting"
            >
              <i v-if="submitting" class="fas fa-spinner fa-spin"></i>
              {{ editingTask ? '更新任务' : '创建任务' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <div :class="['delete-confirm', { active: showDeleteConfirm }]">
      <div class="delete-confirm-content">
        <div class="delete-confirm-header">
          <h3>确认删除</h3>
          <button class="close-btn" @click="closeDeleteConfirm">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="delete-confirm-body">
          <p>确定要删除这个任务吗？此操作不可恢复。</p>
        </div>
        <div class="delete-confirm-actions">
          <button @click="closeDeleteConfirm" class="btn btn-secondary">
            取消
          </button>
          <button
            @click="deleteTask"
            class="btn btn-danger"
            :disabled="deleting"
          >
            <i v-if="deleting" class="fas fa-spinner fa-spin"></i>
            删除
          </button>
        </div>
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
import { ref, reactive, computed, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import duration from 'dayjs/plugin/duration'
import api from '../utils/api'
import { getCurrentUser } from '../utils/auth'

dayjs.extend(relativeTime)
dayjs.extend(duration)

const router = useRouter()
const currentView = ref('next')
const currentUser = ref(null)
const tasks = ref([])
const sortBy = ref('name')
const filterBy = ref('all')
const showTaskModal = ref(false)
const showDeleteConfirm = ref(false)
const editingTask = ref(null)
const taskToDelete = ref(null)
const submitting = ref(false)
const deleting = ref(false)
const taskTitleInput = ref(null)
const taskGrid = ref(null)

const taskForm = reactive({
  title: '',
  description: '',
  deadlineHours: 24
})

const taskFormErrors = reactive({
  title: ''
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
    showToast(error.message || '加载任务失败', 'error')
  }
}

const nextTasks = computed(() => {
  return tasks.value
    .filter(t => t.status !== 'completed')
    .sort((a, b) => new Date(a.created_at) - new Date(b.created_at))
})

const completedTasks = computed(() => {
  return tasks.value
    .filter(t => t.status === 'completed')
    .sort((a, b) => new Date(b.completed_at || b.created_at) - new Date(a.completed_at || a.created_at))
})

const filteredAllTasks = computed(() => {
  let result = [...tasks.value]
  
  if (filterBy.value === 'completed') {
    result = result.filter(t => t.status === 'completed')
  } else if (filterBy.value === 'pending') {
    result = result.filter(t => t.status !== 'completed')
  }
  
  result.sort((a, b) => {
    if (sortBy.value === 'name') {
      return a.title.localeCompare(b.title)
    } else if (sortBy.value === 'createdAt') {
      return new Date(b.created_at) - new Date(a.created_at)
    } else if (sortBy.value === 'status') {
      return (a.status === 'completed' ? 1 : 0) - (b.status === 'completed' ? 1 : 0)
    }
    return 0
  })
  
  return result
})

const getTimeClass = (task) => {
  if (task.status === 'completed') return 'time-completed'
  
  const now = dayjs()
  const deadline = dayjs(task.deadline)
  const diffHours = deadline.diff(now, 'hour')
  
  if (diffHours < 0) return 'time-overdue'
  else if (diffHours < 24) return 'time-countdown'
  else return ''
}

const formatTime = (task) => {
  if (task.status === 'completed') {
    return '已完成'
  }
  
  const now = dayjs()
  const deadline = dayjs(task.deadline)
  const diffHours = deadline.diff(now, 'hour')
  const diffMinutes = deadline.diff(now, 'minute')
  
  if (diffHours < 0) {
    const overdueHours = Math.abs(diffHours)
    if (overdueHours >= 24) {
      const overdueDays = Math.floor(overdueHours / 24)
      return `已逾期 ${overdueDays} 天`
    } else {
      return `已逾期 ${overdueHours} 小时`
    }
  } else if (diffHours >= 24) {
    const days = Math.floor(diffHours / 24)
    return `${days} 天后到期`
  } else if (diffMinutes < 60) {
    return `${diffMinutes} 分钟后到期`
  } else {
    return `${diffHours} 小时后到期`
  }
}

const expandTask = (task) => {
  console.log('Task expanded:', task)
}

const openTaskModal = () => {
  taskForm.title = ''
  taskForm.description = ''
  taskForm.deadlineHours = 24
  taskFormErrors.title = ''
  
  nextTick(() => {
    showTaskModal.value = true
    taskTitleInput.value?.focus()
  })
}

const closeTaskModal = () => {
  showTaskModal.value = false
  editingTask.value = null
}

const editTask = (task) => {
  taskForm.title = task.title
  taskForm.description = task.description || ''
  taskForm.deadlineHours = 24
  taskFormErrors.title = ''
  
  nextTick(() => {
    editingTask.value = task
    showTaskModal.value = true
    taskTitleInput.value?.focus()
  })
}

const submitTask = async () => {
  if (!taskForm.title.trim()) {
    taskFormErrors.title = '任务名称不能为空'
    return
  }
  
  if (taskForm.deadlineHours < 1 || taskForm.deadlineHours > 8760) {
    showToast('期限必须在1-8760小时之间', 'error')
    return
  }
  
  taskFormErrors.title = ''
  submitting.value = true
  
  try {
    const deadline = dayjs().add(taskForm.deadlineHours, 'hour').toISOString()
    
    const data = {
      title: taskForm.title.trim(),
      description: taskForm.description.trim() || '',
      deadline: deadline
    }
    
    if (editingTask.value) {
      await api.tasks.update(editingTask.value.id, data)
      showToast('任务更新成功', 'success')
    } else {
      await api.tasks.create(data)
      showToast('任务创建成功', 'success')
    }
    
    await loadTasks()
    closeTaskModal()
  } catch (error) {
    showToast(error.message || (editingTask.value ? '更新任务失败' : '创建任务失败'), 'error')
  } finally {
    submitting.value = false
  }
}

const completeTask = async (task) => {
  try {
    await api.tasks.partialUpdate(task.id, { status: 'completed' })
    showToast('任务已完成', 'success')
    await loadTasks()
  } catch (error) {
    showToast(error.message || '完成任务失败', 'error')
  }
}

const uncompleteTask = async (task) => {
  try {
    await api.tasks.partialUpdate(task.id, { status: 'pending' })
    showToast('任务已恢复', 'success')
    await loadTasks()
  } catch (error) {
    showToast(error.message || '恢复任务失败', 'error')
  }
}

const confirmDeleteTask = (task) => {
  taskToDelete.value = task
  showDeleteConfirm.value = true
}

const closeDeleteConfirm = () => {
  showDeleteConfirm.value = false
  taskToDelete.value = null
}

const deleteTask = async () => {
  if (!taskToDelete.value) return
  
  deleting.value = true
  const taskId = taskToDelete.value.id
  
  try {
    await api.tasks.delete(taskId)
    showToast('任务已删除', 'success')
    await loadTasks()
    closeDeleteConfirm()
  } catch (error) {
    showToast(error.message || '删除任务失败', 'error')
    await loadTasks()
  } finally {
    deleting.value = false
  }
}

const getLazyImageSrc = (task) => {
  if (task.status === 'completed') {
    return '/images/good.svg'
  }
  
  const now = dayjs()
  const deadline = dayjs(task.deadline)
  const diffHours = deadline.diff(now, 'hour')
  
  if (diffHours < 0) {
    return '/images/lose.svg'
  }
  
  return '/images/proceed.svg'
}

const onImageLoad = (event) => {
  event.target.classList.add('loaded')
}

const onImageError = (event, task) => {
  if (task.status === 'completed') {
    event.target.src = '/images/good.svg'
  } else {
    const now = dayjs()
    const deadline = dayjs(task.deadline)
    const diffHours = deadline.diff(now, 'hour')
    
    if (diffHours < 0) {
      event.target.src = '/images/lose.svg'
    } else {
      event.target.src = '/images/proceed.svg'
    }
  }
}

const logout = () => {
  api.auth.logout()
  router.push('/login')
}

onMounted(() => {
  currentUser.value = getCurrentUser()
  loadTasks()
})

watch(currentView, (newView) => {
  nextTick(() => {
    if (taskGrid.value) {
      taskGrid.value.style.animation = 'none'
      taskGrid.value.offsetHeight
      taskGrid.value.style.animation = 'fadeIn 0.3s ease'
    }
  })
})
</script>