import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI 

load_dotenv()

def get_llm(temperature=0):
    """
    Connects to Gemini 2.5 Flash via OpenRouter.
    """
    return ChatOpenAI(
        model='google/gemini-2.5-flash', # OpenRouter's specific model ID
        openai_api_key=os.getenv("OPENROUTER_API_KEY"), 
        openai_api_base='https://openrouter.ai/api/v1', 
        max_tokens=8192,
        temperature=temperature,
        # OpenRouter likes these optional headers to help track your app
        default_headers={
            "HTTP-Referer": "http://localhost:3000", 
            "X-Title": "Agentic Game Builder"
        }
    )

