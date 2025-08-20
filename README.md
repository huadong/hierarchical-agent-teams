# Preparing

> pip install -U langchain_community tiktoken langchain-openai langchain-cohere langchainhub chromadb langchain langgraph  tavily-python django daphne channels channels_redis django-cors-headers

# Run

## API Key

> src/backend/env.py
>
> ```python
> # LLM Model
> os.environ["LLM_MODEL"] = "qwen-max" # gpt-5 for openai
> os.environ["EMBEDDING_MODEL"] = "text-embedding-v1" # text-embedding-ada-002 for openai
>
> # openai
> # os.environ["OPENAI_API_KEY"] = "YOUR OPENAI API KEY"
> # os.environ["OPENAI_PROJECT_ID"] = "YOUR OPENAI PROJECT ID"
>
> # Tavily
> os.environ["TAVILY_API_KEY"] = "YOUR TAVILY API KEY"
> # LangSmith
> os.environ["LANGSMITH_API_KEY"] = "YOUR LANGCHAIN API KEY"
>
> # DashScope
> os.environ["DASHSCOPE_API_KEY"] = "YOUR QWEN API KEY"
>
> # User Agent
> os.environ["USER_AGENT"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Safari/605.1.15"
>
> ```
>
> set os.environ["DASHSCOPE_API_KEY"] if use qwen-max as LLM
> set os.environ["OPENAI_API_KEY"] and os.environ["OPENAI_PROJECT_ID"] if use openai as LLM

## Build Frontend

> cd src/frontend
>
> npm install
>
> npm run build:deploy

## Run Web Server

> python src/backend/manage.py runserver

## Run Channels Worker

> python manage.py runworker ask_openai_channel

***Notice: run a redis server before run web server and channels worker***
