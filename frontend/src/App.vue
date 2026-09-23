<script setup lang="ts">
import DownloadPanel from './components/DownloadPanel.vue'
import ProgressPanel from './components/ProgressPanel.vue'
import ResultViewer from './components/ResultViewer.vue'
import UrlInput from './components/UrlInput.vue'
</script>

<template>
  <div id="app">
    <h1>Security Audit (ГОСТ Р 56939-2024)</h1>
    <UrlInput />
    <ProgressPanel />
    <ResultViewer />
    <DownloadPanel />
  </div>
</template>

<style scoped>
#app {
  max-width: 960px;
  margin: 0 auto;
  padding: 2rem;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}
</style>
