import os
import keyring
from langchain_ollama import ChatOllama

# LangSmith Set-Up
SERVICE = "langsmith"
USERNAME = "api_key"
os.environ["LANGSMITH_API_KEY"] = keyring.get_password(SERVICE, USERNAME)
os.environ["LANGSMITH_PROJECT"] = "creative_writing_team"
os.environ["LANGSMITH_TRACING"] = "true"

# Define Local LLM
model_name = "gemma3:4b" # "gpt-oss:20b"

llm = ChatOllama(model=model_name, temperature=0.5, validate_model_on_init=True) 

### High Temp
llm_high_temp = ChatOllama(model=model_name, temperature=1.3, validate_model_on_init=True)

### Low Temp
llm_low_temp = ChatOllama(model=model_name, temperature=0.05, validate_model_on_init=True)