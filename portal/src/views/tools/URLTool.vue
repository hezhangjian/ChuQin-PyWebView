<template>
  <div class="tool-page">
    <div class="tool-header">
      <button class="back-btn" @click="$emit('back')">← 返回</button>
      <h1 class="tool-title">URL编解码工具</h1>
    </div>
    <div class="tool-content">
      <div class="mode-selector">
        <button
          :class="['mode-btn', { active: mode === 'encode' }]"
          @click="mode = 'encode'"
        >
          编码
        </button>
        <button
          :class="['mode-btn', { active: mode === 'decode' }]"
          @click="mode = 'decode'"
        >
          解码
        </button>
      </div>
      <div class="input-section">
        <label>{{ mode === 'encode' ? '原始文本' : '编码文本' }}</label>
        <textarea
          v-model="inputText"
          :placeholder="mode === 'encode' ? '请输入要编码的文本...' : '请输入要解码的URL...'"
          class="input-textarea"
          @input="processURL"
        ></textarea>
      </div>
      <div class="output-section">
        <label>{{ mode === 'encode' ? '编码结果' : '解码结果' }}</label>
        <div class="output-container">
          <textarea
            :value="outputText"
            readonly
            class="output-textarea"
            :placeholder="mode === 'encode' ? '编码结果将显示在这里...' : '解码结果将显示在这里...'"
          ></textarea>
          <button class="copy-btn" @click="copyToClipboard" :disabled="!outputText">
            复制
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from 'vue'

export default defineComponent({
  name: 'URLTool',
  emits: ['back'],
  setup() {
    const mode = ref<'encode' | 'decode'>('encode')
    const inputText = ref('')
    const outputText = ref('')

    const processURL = () => {
      if (!inputText.value.trim()) {
        outputText.value = ''
        return
      }

      try {
        if (mode.value === 'encode') {
          outputText.value = encodeURIComponent(inputText.value)
        } else {
          outputText.value = decodeURIComponent(inputText.value)
        }
      } catch (error) {
        outputText.value = '解码错误：无效的URL编码'
      }
    }

    const copyToClipboard = async () => {
      if (outputText.value) {
        try {
          await navigator.clipboard.writeText(outputText.value)
          alert('已复制到剪贴板')
        } catch (error) {
          console.error('Failed to copy:', error)
        }
      }
    }

    watch([inputText, mode], processURL)

    return {
      mode,
      inputText,
      outputText,
      processURL,
      copyToClipboard
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
  max-width: 800px;
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
  max-width: 800px;
  margin: 0 auto;
  background: white;
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.mode-selector {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
}

.mode-btn {
  flex: 1;
  padding: 12px 24px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  color: #2c3e50;
  transition: all 0.2s;
}

.mode-btn:hover {
  border-color: #4a90e2;
  background: #f0f7ff;
}

.mode-btn.active {
  background: #4a90e2;
  color: white;
  border-color: #4a90e2;
}

.input-section,
.output-section {
  margin-bottom: 24px;
}

.input-section:last-child,
.output-section:last-child {
  margin-bottom: 0;
}

label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 8px;
}

.input-textarea,
.output-textarea {
  width: 100%;
  min-height: 200px;
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
  font-family: 'Monaco', 'Menlo', monospace;
  resize: vertical;
  transition: border-color 0.2s;
}

.input-textarea:focus {
  outline: none;
  border-color: #4a90e2;
}

.output-textarea {
  background: #f8f9fa;
  color: #2c3e50;
}

.output-container {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.copy-btn {
  padding: 12px 24px;
  background: #4a90e2;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.2s;
  align-self: flex-end;
}

.copy-btn:hover:not(:disabled) {
  background: #357abd;
  transform: translateY(-1px);
}

.copy-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style>
