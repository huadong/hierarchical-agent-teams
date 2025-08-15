import getpass
import os

def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")


# _set_env("OPENAI_API_KEY")
# _set_env("COHERE_API_KEY")
# _set_env("TAVILY_API_KEY")

# LLM Model
os.environ["LLM_MODEL"] = "qwen-max" # gpt-5 for openai
os.environ["EMBEDDING_MODEL"] = "text-embedding-v1" # text-embedding-ada-002 for openai

# openai
# os.environ["OPENAI_API_KEY"] = "YOUR OPENAI API KEY"
# os.environ["OPENAI_PROJECT_ID"] = "YOUR OPENAI PROJECT ID"

# Tavily
os.environ["TAVILY_API_KEY"] = "YOUR TAVILY API KEY"
# LangSmith
os.environ["LANGSMITH_API_KEY"] = "YOUR LANGCHAIN API KEY"

# DashScope
os.environ["DASHSCOPE_API_KEY"] = "YOUR QWEN API KEY"

# User Agent
os.environ["USER_AGENT"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Safari/605.1.15"
