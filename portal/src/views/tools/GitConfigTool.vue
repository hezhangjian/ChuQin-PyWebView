<template>
  <div class="tool-page">
    <div class="tool-header">
      <button class="back-btn" @click="$emit('back')">← 返回</button>
      <h1 class="tool-title">GitConfig管理工具</h1>
      <button class="refresh-btn" @click="loadConfig">刷新</button>
    </div>
    <div class="tool-content">
      <div class="config-path">
        <label>配置文件路径</label>
        <input :value="configPath" readonly class="path-input" />
      </div>

      <div v-if="error" class="error-message">
        {{ error }}
      </div>

      <div class="config-list">
        <div class="list-header">
          <h2>配置项列表</h2>
          <button class="add-btn" @click="showAddDialog = true">+ 添加配置</button>
        </div>

        <div v-if="loading" class="loading">加载中...</div>
        
        <div v-else-if="configEntries.length === 0" class="empty-state">
          暂无配置项
        </div>

        <div v-else class="entries-container">
          <div
            v-for="(entry, index) in configEntries"
            :key="index"
            class="config-entry"
            :class="{ disabled: entry.disabled, section: entry.type === 'section' }"
          >
            <div v-if="entry.type === 'section'" class="section-entry">
              <span class="section-label">
                [{{ entry.section }}{{ entry.subsection ? ` "${entry.subsection}"` : '' }}]
              </span>
              <div class="entry-actions">
                <button
                  class="toggle-btn"
                  @click="toggleEntry(index)"
                  :title="entry.disabled ? '启用' : '禁用'"
                >
                  {{ entry.disabled ? '启用' : '禁用' }}
                </button>
              </div>
            </div>
            
            <div v-else-if="entry.type === 'config'" class="config-entry-item">
              <div class="config-key-value">
                <span class="config-key">{{ getFullKey(entry) }}</span>
                <span class="config-value">{{ entry.value }}</span>
              </div>
              <div class="entry-actions">
                <button
                  class="toggle-btn"
                  @click="toggleEntry(index)"
                  :title="entry.disabled ? '启用' : '禁用'"
                >
                  {{ entry.disabled ? '启用' : '禁用' }}
                </button>
                <button class="delete-btn" @click="deleteEntry(index)">删除</button>
              </div>
            </div>
            
            <div v-else-if="entry.type === 'empty'" class="empty-line"></div>
            
            <div v-else class="raw-line">
              <code>{{ entry.raw }}</code>
            </div>
          </div>
        </div>
      </div>

      <div class="actions-bar">
        <button class="save-btn" @click="saveConfig" :disabled="loading || saving">
          {{ saving ? '保存中...' : '保存配置' }}
        </button>
      </div>
    </div>

    <!-- Add Config Dialog -->
    <div v-if="showAddDialog" class="dialog-overlay" @click="showAddDialog = false">
      <div class="dialog" @click.stop>
        <div class="dialog-header">
          <h3>添加配置项</h3>
          <button class="close-btn" @click="showAddDialog = false">×</button>
        </div>
        <div class="dialog-content">
          <div class="form-group">
            <label>Section</label>
            <input v-model="newConfig.section" placeholder="例如: user" />
          </div>
          <div class="form-group">
            <label>Subsection (可选)</label>
            <input v-model="newConfig.subsection" placeholder="例如: name" />
          </div>
          <div class="form-group">
            <label>Key</label>
            <input v-model="newConfig.key" placeholder="例如: email" />
          </div>
          <div class="form-group">
            <label>Value</label>
            <input v-model="newConfig.value" placeholder="例如: user@example.com" />
          </div>
        </div>
        <div class="dialog-actions">
          <button class="cancel-btn" @click="showAddDialog = false">取消</button>
          <button class="confirm-btn" @click="addConfig">添加</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'

interface ConfigEntry {
  type: string
  line_number?: number
  section?: string
  subsection?: string
  key?: string
  value?: string
  disabled?: boolean
  raw?: string
}

declare global {
  interface Window {
    pywebview?: {
      api: {
        read_gitconfig: () => Promise<{ success: boolean; entries: ConfigEntry[]; raw_content?: string; error?: string }>
        write_gitconfig: (entries: ConfigEntry[]) => Promise<{ success: boolean; error?: string }>
        get_gitconfig_path: () => Promise<string>
      }
    }
  }
}

export default defineComponent({
  name: 'GitConfigTool',
  emits: ['back'],
  setup() {
    const configPath = ref('')
    const configEntries = ref<ConfigEntry[]>([])
    const loading = ref(false)
    const saving = ref(false)
    const error = ref('')
    const showAddDialog = ref(false)
    const newConfig = ref({
      section: '',
      subsection: '',
      key: '',
      value: ''
    })

    const waitForApi = (maxAttempts = 50): Promise<any> => {
      return new Promise((resolve, reject) => {
        let attempts = 0
        const checkApi = () => {
          attempts++
          const api = (window as any).pywebview?.api || window.pywebview?.api
          if (api) {
            resolve(api)
          } else if (attempts >= maxAttempts) {
            reject(new Error('Python API not available after waiting. Please ensure the application is running in pywebview.'))
          } else {
            setTimeout(checkApi, 100)
          }
        }
        checkApi()
      })
    }

    const getApi = async () => {
      // Try immediate access first
      const api = (window as any).pywebview?.api || window.pywebview?.api
      if (api) {
        return api
      }
      // Wait for API to be available
      return await waitForApi()
    }

    const loadConfig = async () => {
      loading.value = true
      error.value = ''
      try {
        const api = await getApi()
        console.log('API obtained:', api)
        console.log('API keys:', Object.keys(api || {}))
        
        // Check available methods
        const availableMethods = Object.keys(api || {})
        console.log('Available methods:', availableMethods)
        
        // Try different possible method names
        const getPathMethod = api.get_gitconfig_path || api.getGitconfigPath || api['get_gitconfig_path']
        const readMethod = api.read_gitconfig || api.readGitconfig || api['read_gitconfig']
        
        if (!getPathMethod) {
          throw new Error(`get_gitconfig_path method not found. Available methods: ${availableMethods.join(', ')}`)
        }
        
        const pathResult = await getPathMethod()
        console.log('Config path:', pathResult)
        configPath.value = pathResult || '~/.gitconfig'

        if (!readMethod) {
          throw new Error(`read_gitconfig method not found. Available methods: ${availableMethods.join(', ')}`)
        }
        
        const result = await readMethod()
        console.log('Config read result:', result)
        if (result.success) {
          configEntries.value = result.entries || []
          if (configEntries.value.length === 0) {
            error.value = '配置文件为空或不存在'
          }
        } else {
          error.value = result.error || '读取配置失败'
        }
      } catch (err: any) {
        error.value = err.message || '加载配置失败。请确保在 pywebview 环境中运行。'
        console.error('Error loading config:', err)
      } finally {
        loading.value = false
      }
    }

    const saveConfig = async () => {
      saving.value = true
      error.value = ''
      try {
        const api = await getApi()
        const writeMethod = api.write_gitconfig || api.writeGitconfig || api['write_gitconfig']
        if (!writeMethod) {
          throw new Error('write_gitconfig method not found')
        }
        const result = await writeMethod(configEntries.value)
        if (result.success) {
          alert('配置保存成功')
          await loadConfig()
        } else {
          error.value = result.error || '保存配置失败'
        }
      } catch (err: any) {
        error.value = err.message || '保存配置失败'
        console.error('Error saving config:', err)
      } finally {
        saving.value = false
      }
    }

    const toggleEntry = (index: number) => {
      const entry = configEntries.value[index]
      if (entry.type === 'section' || entry.type === 'config') {
        entry.disabled = !entry.disabled
        // Update raw line
        if (entry.type === 'section') {
          const section = entry.section || ''
          const subsection = entry.subsection
          const sectionStr = subsection 
            ? `[${section} "${subsection}"]`
            : `[${section}]`
          entry.raw = entry.disabled ? `# ${sectionStr}` : sectionStr
        } else if (entry.type === 'config') {
          const configLine = `${entry.key} = ${entry.value}`
          entry.raw = entry.disabled ? `# ${configLine}` : configLine
        }
      }
    }

    const deleteEntry = (index: number) => {
      if (confirm('确定要删除此配置项吗？')) {
        configEntries.value.splice(index, 1)
      }
    }

    const addConfig = () => {
      if (!newConfig.value.section || !newConfig.value.key || !newConfig.value.value) {
        alert('请填写完整的配置信息')
        return
      }

      // Find the position to insert (after the last entry or at the end)
      let insertIndex = configEntries.value.length
      
      // Try to find existing section
      for (let i = configEntries.value.length - 1; i >= 0; i--) {
        const entry = configEntries.value[i]
        if (entry.type === 'section' && 
            entry.section === newConfig.value.section &&
            entry.subsection === newConfig.value.subsection) {
          insertIndex = i + 1
          break
        }
      }

      // If section not found, add section first
      let sectionExists = false
      for (const entry of configEntries.value) {
        if (entry.type === 'section' && 
            entry.section === newConfig.value.section &&
            entry.subsection === newConfig.value.subsection) {
          sectionExists = true
          break
        }
      }

      if (!sectionExists) {
        const sectionEntry: ConfigEntry = {
          type: 'section',
          section: newConfig.value.section,
          subsection: newConfig.value.subsection || undefined,
          disabled: false,
          raw: newConfig.value.subsection
            ? `[${newConfig.value.section} "${newConfig.value.subsection}"]`
            : `[${newConfig.value.section}]`
        }
        configEntries.value.splice(insertIndex, 0, sectionEntry)
        insertIndex++
      }

      // Add config entry
      const configEntry: ConfigEntry = {
        type: 'config',
        section: newConfig.value.section,
        subsection: newConfig.value.subsection || undefined,
        key: newConfig.value.key,
        value: newConfig.value.value,
        disabled: false,
        raw: `${newConfig.value.key} = ${newConfig.value.value}`
      }
      configEntries.value.splice(insertIndex, 0, configEntry)

      // Reset form
      newConfig.value = {
        section: '',
        subsection: '',
        key: '',
        value: ''
      }
      showAddDialog.value = false
    }

    const getFullKey = (entry: ConfigEntry): string => {
      if (entry.subsection) {
        return `${entry.section}.${entry.subsection}.${entry.key}`
      }
      return `${entry.section}.${entry.key}`
    }

    onMounted(() => {
      console.log('GitConfigTool mounted')
      // Delay loading to ensure pywebview API is ready
      setTimeout(() => {
        loadConfig()
      }, 500)
    })

    return {
      configPath,
      configEntries,
      loading,
      saving,
      error,
      showAddDialog,
      newConfig,
      loadConfig,
      saveConfig,
      toggleEntry,
      deleteEntry,
      addConfig,
      getFullKey
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
  max-width: 1200px;
  margin: 0 auto 32px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.back-btn,
.refresh-btn {
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

.back-btn:hover,
.refresh-btn:hover {
  background: #f0f0f0;
  transform: translateX(-2px);
}

.refresh-btn {
  margin-left: auto;
}

.tool-title {
  font-size: 28px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
}

.tool-content {
  max-width: 1200px;
  margin: 0 auto;
  background: white;
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.config-path {
  margin-bottom: 24px;
}

.config-path label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 8px;
}

.path-input {
  width: 100%;
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
  font-family: 'Monaco', 'Menlo', monospace;
  background: #f8f9fa;
  color: #2c3e50;
}

.error-message {
  padding: 12px;
  background: #fee;
  border: 1px solid #fcc;
  border-radius: 8px;
  color: #c33;
  margin-bottom: 24px;
}

.config-list {
  margin-bottom: 24px;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.list-header h2 {
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
}

.add-btn {
  padding: 8px 16px;
  background: #4a90e2;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.2s;
}

.add-btn:hover {
  background: #357abd;
  transform: translateY(-1px);
}

.loading,
.empty-state {
  text-align: center;
  padding: 40px;
  color: #7f8c8d;
}

.entries-container {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
}

.config-entry {
  padding: 12px 16px;
  border-bottom: 1px solid #f0f0f0;
  transition: background 0.2s;
}

.config-entry:last-child {
  border-bottom: none;
}

.config-entry:hover {
  background: #f8f9fa;
}

.config-entry.disabled {
  opacity: 0.6;
  background: #f5f5f5;
}

.config-entry.section {
  background: #f0f7ff;
  font-weight: 600;
}

.section-entry {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-label {
  font-family: 'Monaco', 'Menlo', monospace;
  color: #2c3e50;
}

.config-entry-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.config-key-value {
  flex: 1;
  display: flex;
  gap: 16px;
}

.config-key {
  font-family: 'Monaco', 'Menlo', monospace;
  font-weight: 600;
  color: #2c3e50;
  min-width: 200px;
}

.config-value {
  font-family: 'Monaco', 'Menlo', monospace;
  color: #7f8c8d;
}

.entry-actions {
  display: flex;
  gap: 8px;
}

.toggle-btn,
.delete-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.2s;
}

.toggle-btn {
  background: #f0f0f0;
  color: #2c3e50;
}

.toggle-btn:hover {
  background: #e0e0e0;
}

.delete-btn {
  background: #fee;
  color: #c33;
}

.delete-btn:hover {
  background: #fcc;
}

.empty-line {
  height: 8px;
}

.raw-line {
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 12px;
  color: #7f8c8d;
}

.actions-bar {
  display: flex;
  justify-content: flex-end;
  padding-top: 24px;
  border-top: 1px solid #e0e0e0;
}

.save-btn {
  padding: 12px 24px;
  background: #4a90e2;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.2s;
}

.save-btn:hover:not(:disabled) {
  background: #357abd;
  transform: translateY(-1px);
}

.save-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

/* Dialog Styles */
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.dialog {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e0e0e0;
}

.dialog-header h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  color: #7f8c8d;
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s;
}

.close-btn:hover {
  background: #f0f0f0;
  color: #2c3e50;
}

.dialog-content {
  padding: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 8px;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: #4a90e2;
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 20px 24px;
  border-top: 1px solid #e0e0e0;
}

.cancel-btn,
.confirm-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.2s;
}

.cancel-btn {
  background: #f0f0f0;
  color: #2c3e50;
}

.cancel-btn:hover {
  background: #e0e0e0;
}

.confirm-btn {
  background: #4a90e2;
  color: white;
}

.confirm-btn:hover {
  background: #357abd;
}
</style>
