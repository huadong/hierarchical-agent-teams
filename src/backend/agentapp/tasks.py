# your_app/tasks.py
import openai
import os
import asyncio
from langchain_core.prompts import ChatPromptTemplate

from channels.layers import get_channel_layer

import env
from agent.llm import get_llm

from channels.consumer import AsyncConsumer
import asyncio

class AskOpenaiConsumer(AsyncConsumer):
  async def ask_openai(self, event):
      job_id = event.get("job_id")
      question = event.get('question')
      session_id = event.get('session_id')

      print(f"Start job {job_id}, Question: {question} from session {session_id}")
      channel_layer = get_channel_layer()
      
      # bind the task to a group
      group_name = f"stream_{session_id}"
      
      try:
          llm = get_llm(os.environ.get("LLM_MODEL"), streaming=True)
          # Define a prompt template
          prompt = ChatPromptTemplate.from_messages([
              ("system", "You are a helpful assistant. Provide a detailed answer."),
              ("user", "{question}")
          ])

          # Create a chain by piping the prompt to the LLM
          chain = prompt | llm
          # Invoke the chain using the .stream() method
          # This returns an iterator
          async for chunk in chain.astream({"question": question}):
              # The chunk is an AIMessageChunk object
              # We access the content and print it
              if chunk.content:
                  await channel_layer.group_send(
                      group_name,
                      {
                          "type": "stream.message",
                          "message": chunk.content,
                      }
                  )
      except Exception as e:
          await channel_layer.group_send(
              group_name,
              {
                  "type": "stream.message",
                  "message": f"Error: {str(e)}",
              }
          )
      finally:
          # send end message
          await channel_layer.group_send(
              group_name,
              {
                  "type": "stream.message",
                  "message": "[DONE]",
              }
          )