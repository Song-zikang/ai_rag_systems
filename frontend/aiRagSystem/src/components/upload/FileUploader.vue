<template>
  <div class="section">
    <div class="section-label">
      <span class="icon-folder">📂</span>
      <span>Upload Document (TXT only)</span>
    </div>
    
    <div 
      class="upload-area"
      @dragover.prevent
      @dragleave.prevent
      @drop.prevent="handleDrop"
      @click="triggerFileInput"
    >
      <div class="upload-icon">
        <svg width="60" height="50" viewBox="0 0 60 50" fill="none">
          <path d="M30 5L45 20H37.5V35H22.5V20H15L30 5Z" fill="#909399"/>
          <path d="M10 30C10 24.4771 14.4771 20 20 20C22.0089 20 23.8871 20.6636 25.4142 21.764L30 25.3536L34.5858 21.764C36.1129 20.6636 37.9911 20 40 20C45.5228 20 50 24.4771 50 30C50 35.5228 45.5228 40 40 40H20C14.4771 40 10 35.5228 10 30Z" fill="#909399"/>
        </svg>
      </div>
      <div class="upload-text">
        <span v-if="!fileName">Drag file here or <em>click to upload</em></span>
        <span v-else class="success-text">Uploaded: {{ fileName }}</span>
      </div>
      <div class="upload-tip" v-if="!fileName">Only .txt files (max 50MB)</div>
    </div>

    <div class="file-actions" v-if="fileName">
      <button class="action-btn reset-btn" @click.stop="resetFile">
        Reupload
      </button>
      <button class="action-btn clear-btn" @click.stop="clearFile">
        Cancel
      </button>
    </div>

    <input 
      type="file" 
      ref="fileInput" 
      style="display: none" 
      accept=".txt"
      @change="handleFileSelect"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const fileName = ref('')
const fileInput = ref(null)
const baseUrl = 'http://localhost:8000'
const uploadUrl = `${baseUrl}/upload`

const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileSelect = (e) => {
  const file = e.target.files?.[0]
  if (file) validateAndUpload(file)
}

const handleDrop = (e) => {
  const file = e.dataTransfer.files?.[0]
  if (file) validateAndUpload(file)
}

const validateAndUpload = async (file) => {
  const fileExt = file.name.split('.').pop().toLowerCase()
  const isTxt = fileExt === 'txt'
  const maxSize = 50 * 1024 * 1024
  const isSizeValid = file.size <= maxSize

  if (!isTxt) {
    alert('Only TXT files are allowed!')
    return
  }
  if (!isSizeValid) {
    alert(`File size cannot exceed 50MB. Current: ${(file.size/1024/1024).toFixed(2)}MB`)
    return
  }

  const formData = new FormData()
  formData.append('file', file)
  try {
    await axios.post(uploadUrl, formData, { timeout: 60000 })
    fileName.value = file.name
  } catch (err) {
    const errorMsg = err.response?.data?.detail 
      ? `Upload failed: ${err.response.data.detail}`
      : `Upload failed: ${err.message}`
    alert(errorMsg)
  }
}

const resetFile = () => {
  fileName.value = ''
  fileInput.value.value = ''
  triggerFileInput()
}

const clearFile = () => {
  fileName.value = ''
  fileInput.value.value = ''
}

defineExpose({ fileName, clearFile })
</script>

<style scoped lang="scss">
@use "@/assets/styles/variables.scss" as *;

.section {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;

  .section-label {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 18px;
    color: #4a5568;
    font-weight: 600;

    span[class^="icon-"] {
      font-size: 22px;
    }
  }
}

.upload-area {
  width: 100%;
  height: 240px;
  border: 2px dashed #cbd5e0;
  border-radius: $radius;
  background: #fafbfc;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;

  &:hover {
    border-color: $primary;
    background: #f7fafc;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(49, 130, 206, 0.1);
  }
}

.upload-icon {
  margin-bottom: 16px;
  opacity: 0.7;
}

.upload-text {
  font-size: 17px;
  color: #4a5568;
  margin-bottom: 8px;
  font-weight: 500;

  em {
    color: $primary;
    font-style: normal;
    font-weight: 600;
  }
}

.success-text {
  color: $success;
  font-weight: 600;
}

.upload-tip {
  font-size: 14px;
  color: #718096;
}

.file-actions {
  display: flex;
  gap: 12px;
  margin-top: 12px;
}

.action-btn {
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.reset-btn {
  background: #e8f4fd;
  color: $primary;

  &:hover {
    background: #dceefb;
  }
}

.clear-btn {
  background: #fef2f2;
  color: $danger;

  &:hover {
    background: #fee2e2;
  }
}
</style>