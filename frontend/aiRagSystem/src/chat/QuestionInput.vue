<template>
  <div class="section query-section">
    <div class="section-label">
      <span class="icon-chat">💬</span>
      <span>Ask a question</span>
    </div>
    <div class="input-group">
      <input
        :value="question"
        @input="$emit('update:question','$event.target.value')"
        type="text"
        class="question-input"
        placeholder="Enter your question..."
        @keyup.enter="handleAsk"
        :disabled="loading || streamLoading || !hasFile"
      />
      <button
        class="ask-btn"
        :disabled="loading || streamLoading || !hasFile || !question.trim()"
        @click="handleAsk"
      >
        {{ loading || streamLoading ? "Thinking..." : "Submit" }}
      </button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  loading: Boolean,
  streamLoading: Boolean,
  hasFile: Boolean,
  question: String
})
const emit = defineEmits(['update:question', 'ask'])

const handleAsk = () => {
  if (!props.question.trim()) {
    alert('Please enter a question!')
    return
  }
  emit('ask')
}
</script>

<style scoped>
.section {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;
}
.section-label {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  color: #4a5568;
  font-weight: 600;
}
.section-label span[class^="icon-"] {
  font-size: 22px;
}
.input-group {
  display: flex;
  gap: 14px;
  align-items: center;
  width: 100%;
}
.question-input {
  flex: 1;
  height: 56px;
  padding: 0 24px;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  font-size: 17px;
  color: #1a202c;
  outline: none;
  transition: all 0.3s ease;
  background: #fdfdfd;
}
.question-input:focus {
  border-color: #3182ce;
  box-shadow: 0 0 0 3px rgba(49, 130, 206, 0.15);
  background: #ffffff;
}
.question-input:disabled {
  background: #f7fafc;
  color: #a0aec0;
  cursor: not-allowed;
}
.ask-btn {
  padding: 0 32px;
  height: 56px;
  background: #3182ce;
  color: #fff;
  border: none;
  border-radius: 12px;
  font-size: 17px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}
.ask-btn:hover:not(:disabled) {
  background: #2b6cb0;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(49, 130, 206, 0.2);
}
.ask-btn:disabled {
  background: #90cdf4;
  cursor: not-allowed;
}
</style>