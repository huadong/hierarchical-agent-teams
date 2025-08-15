<script setup lang="ts">
import { ref, reactive, nextTick, watch } from 'vue'
import ChatMessage from './ChatMessage.vue'

interface Message {
  id: number
  text: string
  sender: 'user' | 'ai'
  timestamp: Date
}

const messages = ref<Message[]>([
  {
    id: 1,
    text: 'Hello! I am your AI assistant. How can I help you today?',
    sender: 'ai',
    timestamp: new Date()
  }
])
const scrollContainer = ref<HTMLElement | null>(null)

const inputText = ref('')
const isLoading = ref(false)

// Function to scroll to bottom
const scrollToBottom = () => {
  nextTick(() => {
    if (scrollContainer.value) {
      scrollContainer.value.scrollTo({
        top: scrollContainer.value.scrollHeight,
        behavior: 'smooth'
      })
    }
  })
}

// Watch for changes in messages and scroll to bottom
watch(
  () => messages.value,
  () => {
    scrollToBottom()
  },
  { deep: true, immediate: true }
)

const sendMessage = async () => {
  if (!inputText.value.trim() || isLoading.value) return

  // Add user message
  const userMessage: Message = {
    id: Date.now(),
    text: inputText.value,
    sender: 'user',
    timestamp: new Date()
  }
  
  messages.value.push(userMessage)
  const userInput = inputText.value
  inputText.value = ''
  isLoading.value = true

  try {
    // // Simulate API call to AI
    // const aiResponse = await fetchAIResponse(userInput)
    
    // // Add AI response
    // const aiMessage: Message = {
    //   id: Date.now() + 1,
    //   text: aiResponse,
    //   sender: 'ai',
    //   timestamp: new Date()
    // }
    
    // messages.value.push(aiMessage)
    const response = await fetch('http://127.0.0.1:8000/agentapp/question', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no'
        // Add any authentication headers if needed
      },
      body: JSON.stringify({ "question": userInput }),
    });

    if (!response.ok || !response.body) {
      throw new Error('Network response was not ok or streaming is not supported.');
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    let fullContent = '';
    let aiResponseAdded = false;

    // Function to update the chat state incrementally
    const updateMessageContent = (content: string) => {
      // update the latest ai message or create a new one if needed
      const latestMessage = messages.value[messages.value.length - 1];

      if (latestMessage.sender === 'ai') {
        latestMessage.text = content;
      } else {
        // Add a new assistant message if there's no existing one
        const aiResponse: Message = {
          id: Date.now(),
          text: content,
          sender: 'ai',
          timestamp: new Date()
        };

        messages.value.push(aiResponse);
        aiResponseAdded = true;
      }
      return {
        messages: messages,
        isLoading: true,
      };
    };

    // Process the stream
    const processStream = async () => {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const jsonObjects = [];
        let currentChunk = chunk.trim();

        // Handle multiple JSON objects in one chunk
        while (currentChunk) {
          try {
            // Try to parse the current chunk as a complete JSON object
            const parsed = JSON.parse(currentChunk);
            jsonObjects.push(parsed);
            break; // If successful, exit the loop
          } catch (parseError) {
            // If parsing fails, try to find the boundary of the first complete JSON object
            let braceCount = 0;
            let inString = false;
            let escapeNext = false;
            
            for (let i = 0; i < currentChunk.length; i++) {
              const char = currentChunk[i];
              
              if (escapeNext) {
                escapeNext = false;
                continue;
              }
              
              if (char === '\\') {
                escapeNext = true;
                continue;
              }
              
              if (char === '"' && !escapeNext) {
                inString = !inString;
                continue;
              }
              
              if (!inString) {
                if (char === '{' || char === '[') {
                  braceCount++;
                } else if (char === '}' || char === ']') {
                  braceCount--;
                }
                
                // If we've closed all braces, we might have a complete object
                if (braceCount === 0 && (char === '}' || char === ']')) {
                  try {
                    const potentialJson = currentChunk.substring(0, i + 1);
                    const parsed = JSON.parse(potentialJson);
                    jsonObjects.push(parsed);
                    // Update the chunk to the remaining part
                    currentChunk = currentChunk.substring(i + 1).trim();
                    break;
                  } catch (innerError) {
                    // Not a valid JSON yet, continue
                  }
                }
              }
            }
            
            // If we couldn't parse anything, break to avoid infinite loop
            if (jsonObjects.length === 0) {
              console.warn('Could not parse JSON chunk:', currentChunk);
              break;
            }
          }
        }

        // Process each JSON object
        for (const json of jsonObjects) {
          let html = '';
          if (json.node) {
            html = '<div style="color: gray;"><b>(' +json.namespace+ ')Node: ' + json.node + '</b><div><i>' + json.value + '</i></div></div>';
          } else {
            // html = '<div><b>Question: </b>' + json.question + '<div><b>Answer: </b><i>' + json.generation + '</i></div></div>';
          }
          fullContent += html;
        }

        // Update the latest assistant message with the streamed content
        updateMessageContent(fullContent);
      }

      // Finalize the assistant message once streaming is complete
      const latestMessage = messages.value[messages.value.length - 1];

      if (latestMessage.sender === 'ai') {
        latestMessage.text = fullContent;
        return {
          messages: messages,
          isLoading: false,
        };
      }

      return {
        ...messages.value,
        isLoading: false,
      };
    };

    await processStream();
  } catch (error) {
    const errorMessage: Message = {
      id: Date.now() + 1,
      text: 'Sorry, I encountered an error. Please try again.',
      sender: 'ai',
      timestamp: new Date()
    }
    messages.value.push(errorMessage)
  } finally {
    isLoading.value = false
  }
}

// Simulate AI response
const fetchAIResponse = (userInput: string): Promise<string> => {
  return new Promise((resolve) => {
    setTimeout(() => {
      const responses = [
        `I understand you're asking about "${userInput}". This is a simulated response from the AI assistant.`,
        `Thanks for your message: "${userInput}". In a real application, this would connect to an AI service.`,
        `Interesting point about "${userInput}"! As an AI, I'd provide a detailed response here.`,
        `I've processed your input: "${userInput}". This demo shows how a chat interface would work.`
      ]
      resolve(responses[Math.floor(Math.random() * responses.length)])
    }, 1000)
  })
}

const handleKeyPress = (e: KeyboardEvent) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    sendMessage()
  }
}
</script>

<template>
  <div class="chatbox">
    <div class="chatbox-header">
      <h2>AI Assistant</h2>
    </div>
    
    <div ref="scrollContainer" class="chatbox-messages">
      <ChatMessage 
        v-for="message in messages" 
        :key="message.id"
        :message="message"
      />
      <div v-if="isLoading" class="loading-indicator">
        <div class="typing-indicator">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
    </div>
    
    <div class="chatbox-input">
      <textarea
        v-model="inputText"
        @keydown="handleKeyPress"
        placeholder="Type your message here..."
        :disabled="isLoading"
      ></textarea>
      <button 
        @click="sendMessage" 
        :disabled="!inputText.trim() || isLoading"
        class="send-button"
      >
        Send
      </button>
    </div>
  </div>
</template>

<style lang="less" scoped>
.chatbox {
  width: 100%;
  max-width: 800px;
  height: 80vh;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  
  &-header {
    padding: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    text-align: center;
    
    h2 {
      font-weight: 500;
      font-size: 1.5rem;
    }
  }
  
  &-messages {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 15px;
    background-color: #f9f9f9;
  }
  
  &-input {
    padding: 15px;
    background: white;
    border-top: 1px solid #eee;
    display: flex;
    gap: 10px;
    
    textarea {
      flex: 1;
      padding: 12px 15px;
      border: 1px solid #ddd;
      border-radius: 20px;
      resize: none;
      height: 60px;
      font-family: inherit;
      font-size: 1rem;
      outline: none;
      transition: border-color 0.2s;
      
      &:focus {
        border-color: #667eea;
      }
      
      &:disabled {
        background-color: #f5f5f5;
        cursor: not-allowed;
      }
    }
    
    .send-button {
      padding: 0 25px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border: none;
      border-radius: 20px;
      cursor: pointer;
      font-weight: 500;
      transition: opacity 0.2s;
      
      &:hover:not(:disabled) {
        opacity: 0.9;
      }
      
      &:disabled {
        opacity: 0.6;
        cursor: not-allowed;
      }
    }
  }
}

.loading-indicator {
  display: flex;
  justify-content: flex-start;
  margin-top: 10px;
}

.typing-indicator {
  background: #e5e5ea;
  padding: 10px 15px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  gap: 5px;
  
  span {
    height: 8px;
    width: 8px;
    background: #888;
    border-radius: 50%;
    display: inline-block;
    animation: typing 1.4s infinite ease-in-out;
    
    &:nth-child(1) {
      animation-delay: 0s;
    }
    
    &:nth-child(2) {
      animation-delay: 0.2s;
    }
    
    &:nth-child(3) {
      animation-delay: 0.4s;
    }
  }
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-5px);
  }
}
</style>