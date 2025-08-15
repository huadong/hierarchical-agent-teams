<script setup lang="ts">
import ChatBox from './components/ChatBox.vue'
</script>

<template>
  <div class="app">
    <ChatBox />
  </div>
</template>

<style lang="less">
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f5f5f5;
}

.app {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>