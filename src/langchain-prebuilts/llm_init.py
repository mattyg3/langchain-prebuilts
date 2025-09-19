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
model_name = "gemma3:4b"

## Set Temps
base_temp = 1.0
high_temp = 1.3
low_temp = 0.05

## Set Other Params
top_k = 64
top_p = 0.95

### Base
llm = ChatOllama(model=model_name
                 , temperature=base_temp
                 , top_k = top_k
                 , top_p = top_p
                 , validate_model_on_init=True) 

### High Temp
llm_high_temp = ChatOllama(model=model_name
                           , temperature=high_temp
                           , top_k = top_k
                           , top_p = top_p
                           , validate_model_on_init=True)

### Low Temp
llm_low_temp = ChatOllama(model=model_name
                          , temperature=low_temp
                          , top_k = top_k
                          , top_p = top_p
                          , validate_model_on_init=True)