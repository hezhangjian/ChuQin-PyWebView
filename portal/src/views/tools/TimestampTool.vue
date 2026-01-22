<template>
  <div class="tool-page">
    <div class="tool-header">
      <button class="back-btn" @click="$emit('back')">← 返回</button>
      <h1 class="tool-title">时间戳转换工具</h1>
    </div>
    <div class="tool-content">
      <div class="conversion-section">
        <div class="input-group">
          <label>时间戳 (秒)</label>
          <input
            v-model="timestampSeconds"
            type="text"
            placeholder="输入时间戳（秒）"
            class="input-field"
            @input="convertFromTimestamp"
          />
        </div>
        <div class="arrow">→</div>
        <div class="input-group">
          <label>时间戳 (毫秒)</label>
          <input
            v-model="timestampMillis"
            type="text"
            placeholder="输入时间戳（毫秒）"
            class="input-field"
            @input="convertFromTimestampMillis"
          />
        </div>
      </div>
      <div class="date-section">
        <div class="input-group">
          <label>日期时间</label>
          <input
            v-model="dateTime"
            type="datetime-local"
            class="input-field"
            @input="convertFromDateTime"
          />
        </div>
        <div class="arrow">→</div>
        <div class="input-group">
          <label>格式化日期</label>
          <input
            :value="formattedDate"
            readonly
            class="output-field"
            placeholder="格式化日期将显示在这里..."
          />
        </div>
      </div>
      <div class="current-time-section">
        <div class="current-time-card">
          <label>当前时间</label>
          <div class="current-time-display">{{ currentTime }}</div>
          <button class="refresh-btn" @click="updateCurrentTime">刷新</button>
        </div>
        <div class="current-time-card">
          <label>当前时间戳</label>
          <div class="current-timestamp-display">
            <div>秒: {{ currentTimestampSeconds }}</div>
            <div>毫秒: {{ currentTimestampMillis }}</div>
          </div>
          <button class="copy-btn" @click="copyCurrentTimestamp">复制时间戳</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, onUnmounted } from 'vue'

export default defineComponent({
  name: 'TimestampTool',
  emits: ['back'],
  setup() {
    const timestampSeconds = ref('')
    const timestampMillis = ref('')
    const dateTime = ref('')
    const formattedDate = ref('')
    const currentTime = ref('')
    const currentTimestampSeconds = ref('')
    const currentTimestampMillis = ref('')
    let timer: number | null = null

    const formatDate = (date: Date): string => {
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      const hours = String(date.getHours()).padStart(2, '0')
      const minutes = String(date.getMinutes()).padStart(2, '0')
      const seconds = String(date.getSeconds()).padStart(2, '0')
      return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
    }

    const updateCurrentTime = () => {
      const now = new Date()
      currentTime.value = formatDate(now)
      currentTimestampSeconds.value = Math.floor(now.getTime() / 1000).toString()
      currentTimestampMillis.value = now.getTime().toString()
    }

    const convertFromTimestamp = () => {
      if (!timestampSeconds.value.trim()) {
        timestampMillis.value = ''
        dateTime.value = ''
        formattedDate.value = ''
        return
      }

      const seconds = parseInt(timestampSeconds.value, 10)
      if (isNaN(seconds)) {
        return
      }

      const date = new Date(seconds * 1000)
      timestampMillis.value = (seconds * 1000).toString()
      dateTime.value = formatDateTimeLocal(date)
      formattedDate.value = formatDate(date)
    }

    const convertFromTimestampMillis = () => {
      if (!timestampMillis.value.trim()) {
        timestampSeconds.value = ''
        dateTime.value = ''
        formattedDate.value = ''
        return
      }

      const millis = parseInt(timestampMillis.value, 10)
      if (isNaN(millis)) {
        return
      }

      const date = new Date(millis)
      timestampSeconds.value = Math.floor(millis / 1000).toString()
      dateTime.value = formatDateTimeLocal(date)
      formattedDate.value = formatDate(date)
    }

    const convertFromDateTime = () => {
      if (!dateTime.value) {
        timestampSeconds.value = ''
        timestampMillis.value = ''
        formattedDate.value = ''
        return
      }

      const date = new Date(dateTime.value)
      if (isNaN(date.getTime())) {
        return
      }

      timestampSeconds.value = Math.floor(date.getTime() / 1000).toString()
      timestampMillis.value = date.getTime().toString()
      formattedDate.value = formatDate(date)
    }

    const formatDateTimeLocal = (date: Date): string => {
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      const hours = String(date.getHours()).padStart(2, '0')
      const minutes = String(date.getMinutes()).padStart(2, '0')
      return `${year}-${month}-${day}T${hours}:${minutes}`
    }

    const copyCurrentTimestamp = async () => {
      const text = `秒: ${currentTimestampSeconds.value}\n毫秒: ${currentTimestampMillis.value}`
      try {
        await navigator.clipboard.writeText(text)
        alert('已复制到剪贴板')
      } catch (error) {
        console.error('Failed to copy:', error)
      }
    }

    onMounted(() => {
      updateCurrentTime()
      timer = window.setInterval(updateCurrentTime, 1000)
    })

    onUnmounted(() => {
      if (timer) {
        clearInterval(timer)
      }
    })

    return {
      timestampSeconds,
      timestampMillis,
      dateTime,
      formattedDate,
      currentTime,
      currentTimestampSeconds,
      currentTimestampMillis,
      convertFromTimestamp,
      convertFromTimestampMillis,
      convertFromDateTime,
      updateCurrentTime,
      copyCurrentTimestamp
    }
  }
})
</script>

<style scoped>
.tool-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 40px 20px;
}

.tool-header {
  max-width: 1000px;
  margin: 0 auto 32px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.back-btn {
  background: white;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  color: #2c3e50;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.2s;
}

.back-btn:hover {
  background: #f0f0f0;
  transform: translateX(-2px);
}

.tool-title {
  font-size: 28px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
}

.tool-content {
  max-width: 1000px;
  margin: 0 auto;
  background: white;
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.conversion-section,
.date-section {
  display: flex;
  align-items: flex-end;
  gap: 16px;
  margin-bottom: 24px;
}

.current-time-section {
  display: flex;
  gap: 16px;
  margin-top: 32px;
  padding-top: 32px;
  border-top: 2px solid #e0e0e0;
}

.current-time-card {
  flex: 1;
  background: #f8f9fa;
  border-radius: 8px;
  padding: 24px;
}

.input-group {
  flex: 1;
}

label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 8px;
}

.input-field {
  width: 100%;
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
  font-family: 'Monaco', 'Menlo', monospace;
  transition: border-color 0.2s;
}

.input-field:focus {
  outline: none;
  border-color: #4a90e2;
}

.output-field {
  width: 100%;
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
  font-family: 'Monaco', 'Menlo', monospace;
  background: #f8f9fa;
  color: #2c3e50;
}

.arrow {
  font-size: 24px;
  color: #4a90e2;
  font-weight: bold;
  padding-bottom: 8px;
}

.current-time-display {
  font-size: 24px;
  font-weight: 600;
  color: #2c3e50;
  margin: 16px 0;
  font-family: 'Monaco', 'Menlo', monospace;
}

.current-timestamp-display {
  font-size: 16px;
  color: #2c3e50;
  margin: 16px 0;
  font-family: 'Monaco', 'Menlo', monospace;
  line-height: 1.8;
}

.refresh-btn,
.copy-btn {
  padding: 10px 20px;
  background: #4a90e2;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.2s;
  width: 100%;
  margin-top: 8px;
}

.refresh-btn:hover,
.copy-btn:hover {
  background: #357abd;
  transform: translateY(-1px);
}
</style>
