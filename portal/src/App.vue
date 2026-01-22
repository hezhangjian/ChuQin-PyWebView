<template>
  <Dashboard v-if="currentView === 'dashboard'" @navigate="handleNavigate" />
  <MD5Tool v-else-if="currentView === 'md5'" @back="handleBack" />
  <URLTool v-else-if="currentView === 'url'" @back="handleBack" />
  <HEXTool v-else-if="currentView === 'hex'" @back="handleBack" />
  <TimestampTool v-else-if="currentView === 'timestamp'" @back="handleBack" />
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import Dashboard from './views/dashboard/Dashboard.vue'
import MD5Tool from './views/tools/MD5Tool.vue'
import URLTool from './views/tools/URLTool.vue'
import HEXTool from './views/tools/HEXTool.vue'
import TimestampTool from './views/tools/TimestampTool.vue'

export default defineComponent({
  name: 'App',
  components: {
    Dashboard,
    MD5Tool,
    URLTool,
    HEXTool,
    TimestampTool
  },
  setup() {
    const currentView = ref<string>('dashboard')

    const handleNavigate = (view: string) => {
      currentView.value = view
    }

    const handleBack = () => {
      currentView.value = 'dashboard'
    }

    return {
      currentView,
      handleNavigate,
      handleBack
    }
  }
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
}
</style>
