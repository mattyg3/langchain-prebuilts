import os
import keyring

SERVICE = "langsmith"
USERNAME = "api_key"
os.environ["LANGSMITH_API_KEY"] = keyring.get_password(SERVICE, USERNAME)

os.environ["LANGSMITH_PROJECT"] = "creative_writing_team"
os.environ["LANGSMITH_TRACING"] = "true"
