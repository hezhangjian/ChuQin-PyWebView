<template>
  <div class="dashboard">
    <div class="container">
      <h1 class="title">ChuQin</h1>
      <div class="tools-grid">
        <div 
          v-for="tool in tools" 
          :key="tool.id"
          class="tool-card"
          @click="handleToolClick(tool)"
        >
          <div class="tool-icon">{{ tool.icon }}</div>
          <div class="tool-title">{{ tool.title }}</div>
          <div class="tool-subtitle">{{ tool.subtitle }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

interface Tool {
  id: string
  title: string
  subtitle: string
  icon: string
}

export default defineComponent({
  name: 'Dashboard',
  emits: ['navigate'],
  setup(_, { emit }) {
    // Define all tools
    const tools: Tool[] = [
      {
        id: 'ppt',
        title: '创建PPT',
        subtitle: '快速创建演示文稿',
        icon: '📊'
      },
      {
        id: 'git-config',
        title: 'GitConfig管理',
        subtitle: 'Git配置管理工具',
        icon: '⚙️'
      },
      {
        id: 'json',
        title: 'JSON格式化',
        subtitle: 'JSON美化与验证工具',
        icon: '📝'
      },
      {
        id: 'md5',
        title: 'MD5',
        subtitle: 'MD5哈希计算工具',
        icon: '🔒'
      },
      {
        id: 'url',
        title: 'URL编解码',
        subtitle: 'URL编码/解码转换',
        icon: '🔗'
      },
      {
        id: 'hex',
        title: 'HEX转换',
        subtitle: '进制转换工具',
        icon: '🔄'
      },
      {
        id: 'timestamp',
        title: '时间戳转换',
        subtitle: '时间戳与日期转换',
        icon: '⏰'
      },
      {
        id: 'huawei-token',
        title: '华为云Token',
        subtitle: '获取华为云访问令牌',
        icon: '🔑'
      }
    ]

    // Handle tool card click
    const handleToolClick = (tool: Tool) => {
      console.log('Tool clicked:', tool.id, tool.title)
      // Emit navigate event for available tools
      const availableTools = ['md5', 'url', 'hex', 'timestamp', 'git-config']
      if (availableTools.includes(tool.id)) {
        console.log('Navigating to:', tool.id)
        emit('navigate', tool.id)
      } else {
        console.log('Clicked tool:', tool.title, '- not available')
        // TODO: Navigate to other tool pages
      }
    }

    return {
      tools,
      handleToolClick
    }
  }
})
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 40px 20px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.title {
  text-align: center;
  font-size: 36px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 40px;
}

.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  padding: 0 20px;
}

.tool-card {
  background: white;
  border-radius: 12px;
  padding: 32px 24px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.tool-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.tool-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.tool-title {
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 8px;
}

.tool-subtitle {
  font-size: 14px;
  color: #7f8c8d;
  line-height: 1.5;
}
</style>
