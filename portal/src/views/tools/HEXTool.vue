<template>
  <div class="tool-page">
    <div class="tool-header">
      <button class="back-btn" @click="$emit('back')">← 返回</button>
      <h1 class="tool-title">HEX进制转换工具</h1>
    </div>
    <div class="tool-content">
      <div class="conversion-section">
        <div class="input-group">
          <label>十进制 (DEC)</label>
          <input
            v-model="decimal"
            type="text"
            placeholder="输入十进制数字"
            class="input-field"
            @input="convertFromDecimal"
          />
        </div>
        <div class="arrow">→</div>
        <div class="input-group">
          <label>十六进制 (HEX)</label>
          <input
            v-model="hex"
            type="text"
            placeholder="输入十六进制数字"
            class="input-field"
            @input="convertFromHex"
          />
        </div>
      </div>
      <div class="conversion-section">
        <div class="input-group">
          <label>二进制 (BIN)</label>
          <input
            v-model="binary"
            type="text"
            placeholder="输入二进制数字"
            class="input-field"
            @input="convertFromBinary"
          />
        </div>
        <div class="arrow">→</div>
        <div class="input-group">
          <label>八进制 (OCT)</label>
          <input
            v-model="octal"
            type="text"
            placeholder="输入八进制数字"
            class="input-field"
            @input="convertFromOctal"
          />
        </div>
      </div>
      <div class="text-conversion-section">
        <div class="input-group">
          <label>文本转HEX</label>
          <textarea
            v-model="textInput"
            placeholder="输入文本"
            class="input-textarea"
            @input="textToHex"
          ></textarea>
        </div>
        <div class="arrow">→</div>
        <div class="input-group">
          <label>HEX转文本</label>
          <div class="output-container">
            <textarea
              :value="hexOutput"
              readonly
              class="output-textarea"
              placeholder="HEX结果"
            ></textarea>
            <button class="copy-btn" @click="copyHex" :disabled="!hexOutput">
              复制
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'

export default defineComponent({
  name: 'HEXTool',
  emits: ['back'],
  setup() {
    const decimal = ref('')
    const hex = ref('')
    const binary = ref('')
    const octal = ref('')
    const textInput = ref('')
    const hexOutput = ref('')

    const convertFromDecimal = () => {
      if (!decimal.value.trim()) {
        hex.value = ''
        binary.value = ''
        octal.value = ''
        return
      }

      const num = parseInt(decimal.value, 10)
      if (isNaN(num)) {
        return
      }

      hex.value = num.toString(16).toUpperCase()
      binary.value = num.toString(2)
      octal.value = num.toString(8)
    }

    const convertFromHex = () => {
      if (!hex.value.trim()) {
        decimal.value = ''
        binary.value = ''
        octal.value = ''
        return
      }

      const num = parseInt(hex.value.replace(/^0x/, ''), 16)
      if (isNaN(num)) {
        return
      }

      decimal.value = num.toString(10)
      binary.value = num.toString(2)
      octal.value = num.toString(8)
    }

    const convertFromBinary = () => {
      if (!binary.value.trim()) {
        decimal.value = ''
        hex.value = ''
        octal.value = ''
        return
      }

      const num = parseInt(binary.value, 2)
      if (isNaN(num)) {
        return
      }

      decimal.value = num.toString(10)
      hex.value = num.toString(16).toUpperCase()
      octal.value = num.toString(8)
    }

    const convertFromOctal = () => {
      if (!octal.value.trim()) {
        decimal.value = ''
        hex.value = ''
        binary.value = ''
        return
      }

      const num = parseInt(octal.value, 8)
      if (isNaN(num)) {
        return
      }

      decimal.value = num.toString(10)
      hex.value = num.toString(16).toUpperCase()
      binary.value = num.toString(2)
    }

    const textToHex = () => {
      if (!textInput.value.trim()) {
        hexOutput.value = ''
        return
      }

      const hexArray = Array.from(textInput.value)
        .map(char => char.charCodeAt(0).toString(16).padStart(2, '0').toUpperCase())
      hexOutput.value = hexArray.join(' ')
    }

    const copyHex = async () => {
      if (hexOutput.value) {
        try {
          await navigator.clipboard.writeText(hexOutput.value)
          alert('已复制到剪贴板')
        } catch (error) {
          console.error('Failed to copy:', error)
        }
      }
    }

    return {
      decimal,
      hex,
      binary,
      octal,
      textInput,
      hexOutput,
      convertFromDecimal,
      convertFromHex,
      convertFromBinary,
      convertFromOctal,
      textToHex,
      copyHex
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

.conversion-section {
  display: flex;
  align-items: flex-end;
  gap: 16px;
  margin-bottom: 24px;
}

.text-conversion-section {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin-top: 32px;
  padding-top: 32px;
  border-top: 2px solid #e0e0e0;
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

.input-textarea {
  width: 100%;
  min-height: 120px;
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
  width: 100%;
  min-height: 120px;
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
