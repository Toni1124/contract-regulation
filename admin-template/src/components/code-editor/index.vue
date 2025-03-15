<template>
  <div class="code-editor" :style="{ height }">
    <MonacoEditor
      v-model:value="code"
      :language="language"
      :theme="theme"
      :options="editorOptions"
      @change="handleChange"
    />
  </div>
</template>

<script lang="ts" setup>
import { ref, watch } from 'vue'
import * as monaco from 'monaco-editor'
import MonacoEditor from '@/components/monaco-editor/index.vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  language: {
    type: String,
    default: 'solidity'
  },
  theme: {
    type: String,
    default: 'vs-dark'
  },
  height: {
    type: String,
    default: '500px'
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

// 编辑器配置
const editorOptions = {
  tabSize: 2,
  fontSize: 14,
  minimap: { enabled: true },
  scrollBeyondLastLine: false,
  automaticLayout: true,
  formatOnPaste: true,
  formatOnType: true
}

// 代码内容
const code = ref(props.modelValue)

// 监听外部值变化
watch(() => props.modelValue, (newVal) => {
  if (newVal !== code.value) {
    code.value = newVal
  }
})

// 监听内部值变化
watch(() => code.value, (newVal) => {
  emit('update:modelValue', newVal)
  emit('change', newVal)
})

// 处理代码变更
const handleChange = (value: string) => {
  code.value = value
}
</script>

<style lang="scss" scoped>
.code-editor {
  width: 100%;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  overflow: hidden;
}
</style> 