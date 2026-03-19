<template>
  <div v-if="answer" class="answer-section">
    <div class="answer-box">
      <div class="answer-header">
        <h3>AI Response</h3>
        <button class="copy-btn" @click="handleCopy">Copy</button>
      </div>
      <div class="divider"></div>
      <div class="answer-text">{{ answer }}</div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({ answer: String })
const emit = defineEmits(['copy'])

const handleCopy = async () => {
  try {
    await navigator.clipboard.writeText(props.answer)
    alert('Copied to clipboard!')
    emit('copy')
  } catch (err) {
    alert('Copy failed!')
  }
}
</script>

<style scoped>
.answer-section {
  margin-top: 8px;
  animation: fadeIn 0.5s ease forwards;
  width: 100%;
}
.answer-box {
  background: #f8fafc;
  border-left: 5px solid #3182ce;
  border-radius: 14px;
  padding: 32px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  width: 100%;
}
.answer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.answer-header h3 {
  font-size: 22px;
  font-weight: 700;
  color: #1a202c;
}
.copy-btn {
  padding: 8px 16px;
  background: transparent;
  color: #3182ce;
  border: 1px solid #3182ce;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}
.copy-btn:hover {
  background: #f7fafc;
}
.divider {
  height: 1px;
  background: #e2e8f0;
  margin-bottom: 24px;
}
.answer-text {
  line-height: 1.8;
  font-size: 17px;
  color: #2d3748;
  white-space: pre-wrap;
  word-break: break-word;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>