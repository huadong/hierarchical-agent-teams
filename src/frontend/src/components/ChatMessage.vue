<script setup lang="ts">
import { computed } from 'vue'
import { marked } from 'marked';

interface Message {
  id: number
  text: string
  sender: 'user' | 'ai'
  timestamp: Date
}

interface Props {
  message: Message
}

const props = defineProps<Props>()

const formatTime = (date: Date) => {
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const parsedMessageText = computed(() => {
  return marked(props.message.text);
})
</script>

<template>
  <div :class="['message', `message--${message.sender}`]">
    <div class="message-content">
      <div class="message-text" v-html="parsedMessageText" />
      <div class="message-time">{{ formatTime(message.timestamp) }}</div>
    </div>
  </div>
</template>

<style lang="less" scoped>
.message {
  display: flex;
  max-width: 80%;
  
  &--user {
    align-self: flex-end;
    .message-content {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border-radius: 18px 18px 4px 18px;
    }
  }
  
  &--ai {
    align-self: flex-start;
    .message-content {
      background: #e5e5ea;
      color: #000;
      border-radius: 18px 18px 18px 4px;
    }
  }
  
  &-content {
    padding: 12px 16px;
    position: relative;
  }
  
  &-text {
    word-wrap: break-word;
    line-height: 1.4;
  }
  
  &-time {
    font-size: 0.7rem;
    text-align: right;
    margin-top: 5px;
    opacity: 0.8;
  }
}
</style>