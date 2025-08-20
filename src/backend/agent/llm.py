from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings

from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

def get_llm(model_name: str = "qwen-max", streaming = False, temperature: float = 0.0):
    """
    Get the LLM instance based on the model name.
    
    Args:
        model_name (str): The name of the model to use.
        temperature (float): The temperature setting for the model.
        
    Returns:
        ChatOpenAI or ChatTongyi: An instance of the specified LLM.
    """
    if model_name == "gpt-5" or model_name == "gpt-4o-mini":
        return ChatOpenAI(model=model_name, streaming=streaming, temperature=temperature)
    elif model_name == "qwen-max":
        return ChatTongyi(model=model_name, temperature=temperature)
    else:
        raise ValueError(f"Unsupported model name: {model_name}")

def get_embeddings(model_name: str = "text-embedding-v1"):
    """
    Get the embeddings instance based on the model name.
    
    Args:
        model_name (str): The name of the embedding model to use.
        
    Returns:
        DashScopeEmbeddings: An instance of the specified embeddings model.
    """
    if model_name == "text-embedding-v1":
        return DashScopeEmbeddings(model=model_name)
    elif model_name == "text-embedding-ada-002":
        return OpenAIEmbeddings(model=model_name)
    else:
        raise ValueError(f"Unsupported embeddings model name: {model_name}")