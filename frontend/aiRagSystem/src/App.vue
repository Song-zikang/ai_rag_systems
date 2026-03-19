<template>
  <div class="app-container">
    <div class="chat-card">
      <Header />
      <FileUploader ref="uploadRef" />
      <QuestionInput
        :loading="loading"
        :streamLoading="streamLoading"
        :has-file="!!uploadRef?.fileName"
        :question="question"
        @update:question="v => question = v"
        @ask="askQuestion"
      />
      <AnswerBox :answer="answer" @copy="copyAnswer" />
    </div>
  </div>
</template>

<script setup>
import { ref} from 'vue'
import Header from './layout/Header.vue'
import FileUploader from './components/upload/FileUploader.vue'
import QuestionInput from './chat/QuestionInput.vue'
import AnswerBox from './chat/AnswerBox.vue'

const question = ref('')
const answer = ref('')
const loading = ref(false)
const streamLoading = ref(false)
const controller = ref(null)
const uploadRef = ref(null)
const baseUrl = 'http://localhost:8000'
const askUrl = `${baseUrl}/ask`

const askQuestion = async () => {
  if (!uploadRef.value?.fileName) {
    alert('Please upload a document first!')
    return
  }
  loading.value = true
  answer.value = ''
  streamLoading.value = true
  controller.value = new AbortController()
  try {
    const response = await fetch(askUrl + `?question=${encodeURIComponent(question.value)}`, {
      method: 'POST',
      signal: controller.value.signal
    })
    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let result = ''
    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      result += decoder.decode(value, { stream: true })
      answer.value = result
    }
  } catch (err) {
    if (err.name !== 'AbortError') alert(`Request failed: ${err.message}`)
  } finally {
    loading.value = false
    streamLoading.value = false
  }
}

const copyAnswer = () => {}
</script>

<style scoped lang="scss">
@use "@/assets/styles/variables.scss" as *;

.app-container {
  width: 100%;
  min-height: 100vh;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 2rem 4rem;
}

.chat-card {
  width: 100%;
  max-width: 100%;
  background: #ffffff;
  border-radius: $radius;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
  padding: 48px 64px;
  display: flex;
  flex-direction: column;
  gap: 32px;
  margin: 0 auto;

  @media (max-width: 768px) {
    padding: 32px 24px;
  }
}
</style>